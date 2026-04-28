"""PDF rendering engine using Playwright (Chromium headless).

Playwright is a 100% pip-managed dependency: `pip install playwright` ships
the Python bindings, and `python -m playwright install chromium` downloads
the Chromium binary into a Playwright-owned cache dir (~/.cache/ms-playwright
on Linux/macOS, %LOCALAPPDATA%/ms-playwright on Windows).

Compared to wkhtmltopdf this gives us:
  - No external system binary, no PATH config, no abandoned upstream.
  - Identical render across Win/Linux/macOS — same Chromium build.
  - JS execution out of the box (MathJax, Mermaid render correctly when their
    scripts are present in the HTML).
"""

from __future__ import annotations

import logging
import subprocess
import sys
from importlib.metadata import PackageNotFoundError as _PkgNotFoundError
from importlib.metadata import version as _pkg_version
from pathlib import Path

from playwright.sync_api import Error as PlaywrightError, sync_playwright

from .converter import convert_to_html

logger = logging.getLogger(__name__)


_VALID_PAGE_FORMATS = {"A4", "A3", "A5", "Letter", "Legal", "Tabloid", "A0", "A1", "A2", "A6"}

_DEFAULT_MARGIN = {
    "top": "20mm",
    "right": "18mm",
    "bottom": "22mm",
    "left": "18mm",
}

try:
    _VERSION = _pkg_version("md-to-pdf")
except _PkgNotFoundError:
    _VERSION = "dev"

_FOOTER_TEMPLATE = f"""
<div style="font-family:'Segoe UI',sans-serif;font-size:8pt;color:#6b7280;
            width:100%;margin:0 18mm;display:flex;justify-content:space-between;align-items:center;">
  <span>Developed by @costamagnus &middot; v{_VERSION}</span>
  <span><span class="pageNumber"></span> / <span class="totalPages"></span></span>
</div>
"""

_HEADER_TEMPLATE = "<div></div>"

_INSTALL_HINT = (
    "Chromium is not installed. Run:\n"
    "    md-to-pdf --install-browser\n"
    "or directly:\n"
    f"    {sys.executable} -m playwright install chromium\n"
    "(one-time download, ~150 MB)"
)


class ChromiumNotInstalledError(RuntimeError):
    """Raised when the Chromium binary required by Playwright is missing."""


def install_browser() -> int:
    """Download the Chromium binary used by the renderer.

    Returns the exit code of `playwright install chromium`. 0 on success.
    """
    logger.info("Installing Chromium via Playwright (this may take a minute)...")
    result = subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        check=False,
    )
    if result.returncode == 0:
        logger.info("Chromium installed successfully.")
    else:
        logger.error("Chromium install failed (exit code %d)", result.returncode)
    return result.returncode


def _is_chromium_missing(exc: PlaywrightError) -> bool:
    msg = str(exc).lower()
    return "executable doesn't exist" in msg or "browsertype.launch" in msg and "install" in msg


def md_to_pdf(
    md_path: Path,
    output_path: Path,
    *,
    css_content: str = "",
    title: str = "",
    page_size: str = "A4",
) -> Path:
    """Convert a Markdown file to PDF via headless Chromium.

    Args:
        md_path: Path to the source `.md` file.
        output_path: Where to write the PDF.
        css_content: Stylesheet injected into the HTML before render.
        title: HTML <title> (defaults to the filename stem).
        page_size: One of A4/A3/A5/Letter/Legal/Tabloid (case-sensitive).

    Raises:
        ChromiumNotInstalledError: if the Chromium binary is missing.
        RuntimeError: for any other Playwright failure.
    """
    if page_size not in _VALID_PAGE_FORMATS:
        logger.warning("Unknown page size %r, falling back to A4", page_size)
        page_size = "A4"

    html_str = convert_to_html(md_path, css=css_content, title=title)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with sync_playwright() as pw:
            try:
                browser = pw.chromium.launch()
            except PlaywrightError as exc:
                if _is_chromium_missing(exc):
                    raise ChromiumNotInstalledError(_INSTALL_HINT) from exc
                raise RuntimeError(f"Failed to launch Chromium: {exc}") from exc

            try:
                page = browser.new_page()
                page.set_content(html_str, wait_until="networkidle")
                page.emulate_media(media="print")
                page.pdf(
                    path=str(output_path),
                    format=page_size,
                    margin=_DEFAULT_MARGIN,
                    print_background=True,
                    display_header_footer=True,
                    header_template=_HEADER_TEMPLATE,
                    footer_template=_FOOTER_TEMPLATE,
                    prefer_css_page_size=False,
                )
            finally:
                browser.close()
    except PlaywrightError as exc:
        raise RuntimeError(f"PDF generation failed: {exc}") from exc

    logger.info("PDF generated → %s", output_path)
    return output_path
