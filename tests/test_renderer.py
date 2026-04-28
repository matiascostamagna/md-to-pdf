"""Tests for the Playwright-based renderer."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from md_to_pdf import renderer
from md_to_pdf.renderer import ChromiumNotInstalledError

FIXTURES = Path(__file__).parent / "fixtures"


def _build_fake_playwright(tmp_path: Path, *, launch_error: Exception | None = None):
    """Build a fake `sync_playwright()` whose context manager mimics the real
    Playwright API (`pw.chromium.launch().new_page().pdf(...)`).

    `launch_error`, if provided, is raised when `chromium.launch()` is called.
    """
    captured: dict = {}

    def fake_pdf(**kwargs) -> None:
        captured["pdf_kwargs"] = kwargs
        Path(kwargs["path"]).write_bytes(b"%PDF-fake")

    def fake_set_content(html: str, **kwargs) -> None:
        captured["html"] = html
        captured["set_content_kwargs"] = kwargs

    page = MagicMock()
    page.pdf.side_effect = fake_pdf
    page.set_content.side_effect = fake_set_content

    browser = MagicMock()
    browser.new_page.return_value = page

    chromium = MagicMock()
    if launch_error is not None:
        chromium.launch.side_effect = launch_error
    else:
        chromium.launch.return_value = browser

    pw_obj = MagicMock()
    pw_obj.chromium = chromium

    ctx = MagicMock()
    ctx.__enter__.return_value = pw_obj
    ctx.__exit__.return_value = False

    factory = MagicMock(return_value=ctx)
    return factory, captured, browser


def test_md_to_pdf_renders_via_playwright(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    factory, captured, browser = _build_fake_playwright(tmp_path)
    monkeypatch.setattr(renderer, "sync_playwright", factory)

    out = tmp_path / "out.pdf"
    result = renderer.md_to_pdf(FIXTURES / "basic.md", out, page_size="Letter")

    assert result == out
    assert out.is_file()
    assert captured["pdf_kwargs"]["format"] == "Letter"
    assert captured["pdf_kwargs"]["print_background"] is True
    assert captured["pdf_kwargs"]["display_header_footer"] is True
    assert "<h1" in captured["html"]
    browser.close.assert_called_once()


def test_md_to_pdf_passes_default_margins(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    factory, captured, _ = _build_fake_playwright(tmp_path)
    monkeypatch.setattr(renderer, "sync_playwright", factory)

    renderer.md_to_pdf(FIXTURES / "basic.md", tmp_path / "out.pdf")

    margin = captured["pdf_kwargs"]["margin"]
    assert margin == {
        "top": "20mm",
        "right": "18mm",
        "bottom": "22mm",
        "left": "18mm",
    }


def test_md_to_pdf_unknown_page_size_falls_back(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    factory, captured, _ = _build_fake_playwright(tmp_path)
    monkeypatch.setattr(renderer, "sync_playwright", factory)

    with caplog.at_level("WARNING"):
        renderer.md_to_pdf(FIXTURES / "basic.md", tmp_path / "out.pdf", page_size="Garbage")

    assert captured["pdf_kwargs"]["format"] == "A4"
    assert any("Unknown page size" in m for m in caplog.messages)


def test_md_to_pdf_closes_browser_on_render_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    factory, _, browser = _build_fake_playwright(tmp_path)
    browser.new_page.return_value.set_content.side_effect = RuntimeError("boom")
    monkeypatch.setattr(renderer, "sync_playwright", factory)

    with pytest.raises(RuntimeError, match="boom"):
        renderer.md_to_pdf(FIXTURES / "basic.md", tmp_path / "out.pdf")

    browser.close.assert_called_once()


def test_md_to_pdf_raises_chromium_not_installed(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from playwright.sync_api import Error as PlaywrightError

    err = PlaywrightError(
        "BrowserType.launch: Executable doesn't exist at C:\\Users\\foo\\chrome.exe\n"
        "Please run: playwright install"
    )
    factory, _, _ = _build_fake_playwright(tmp_path, launch_error=err)
    monkeypatch.setattr(renderer, "sync_playwright", factory)

    with pytest.raises(ChromiumNotInstalledError) as excinfo:
        renderer.md_to_pdf(FIXTURES / "basic.md", tmp_path / "out.pdf")

    assert "--install-browser" in str(excinfo.value)


def test_md_to_pdf_wraps_other_launch_errors(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from playwright.sync_api import Error as PlaywrightError

    err = PlaywrightError("Connection closed unexpectedly")
    factory, _, _ = _build_fake_playwright(tmp_path, launch_error=err)
    monkeypatch.setattr(renderer, "sync_playwright", factory)

    with pytest.raises(RuntimeError, match="Failed to launch Chromium"):
        renderer.md_to_pdf(FIXTURES / "basic.md", tmp_path / "out.pdf")


def test_install_browser_invokes_playwright_cli(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict = {}

    class FakeResult:
        returncode = 0

    def fake_run(cmd, check):
        captured["cmd"] = cmd
        captured["check"] = check
        return FakeResult()

    monkeypatch.setattr(renderer.subprocess, "run", fake_run)
    code = renderer.install_browser()

    assert code == 0
    assert captured["cmd"][1:] == ["-m", "playwright", "install", "chromium"]
    assert captured["check"] is False


def test_install_browser_returns_nonzero_on_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeResult:
        returncode = 7

    monkeypatch.setattr(renderer.subprocess, "run", lambda *a, **k: FakeResult())
    assert renderer.install_browser() == 7


@pytest.mark.skipif(
    not __import__("shutil").which("playwright"),
    reason="playwright CLI not on PATH",
)
def test_md_to_pdf_integration_produces_pdf(tmp_path: Path) -> None:
    """End-to-end sanity check; requires Chromium to be installed."""
    out = tmp_path / "out.pdf"
    try:
        result = renderer.md_to_pdf(FIXTURES / "basic.md", out)
    except ChromiumNotInstalledError:
        pytest.skip("Chromium not installed (run: md-to-pdf --install-browser)")

    assert result == out
    assert out.is_file()
    assert out.read_bytes()[:4] == b"%PDF"
