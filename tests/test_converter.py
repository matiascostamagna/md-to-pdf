"""Tests for the Markdown → HTML conversion engine."""

from __future__ import annotations

import base64
from pathlib import Path

import pytest

from md_to_pdf.converter import convert_to_html

FIXTURES = Path(__file__).parent / "fixtures"


def test_basic_markdown_renders_core_elements() -> None:
    html = convert_to_html(FIXTURES / "basic.md", title="Basic")

    assert "<h1" in html and "Basic Document" in html
    assert "<strong>world</strong>" in html
    assert "<em>italic</em>" in html
    assert "<table>" in html
    assert "<th" in html and "Col A" in html
    assert "highlight" in html or "codehilite" in html
    assert 'lang="en"' in html
    assert "<title>Basic</title>" in html


def test_title_defaults_to_filename_stem() -> None:
    html = convert_to_html(FIXTURES / "basic.md")
    assert "<title>basic</title>" in html


def test_page_break_marker_is_replaced() -> None:
    html = convert_to_html(FIXTURES / "page_break.md")
    assert '<div class="page-break"></div>' in html
    assert "\\newpage" not in html


def test_local_image_is_embedded_as_data_uri(tmp_path: Path) -> None:
    png_bytes = base64.b64decode(
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
    )
    img_path = tmp_path / "sample.png"
    img_path.write_bytes(png_bytes)

    md_path = tmp_path / "doc.md"
    md_path.write_text("# Image\n\n![x](sample.png)\n", encoding="utf-8")

    html = convert_to_html(md_path)
    assert "data:image/png;base64," in html
    assert 'src="sample.png"' not in html


def test_remote_image_is_not_rewritten(tmp_path: Path) -> None:
    md_path = tmp_path / "doc.md"
    md_path.write_text("![x](https://example.com/img.png)\n", encoding="utf-8")

    html = convert_to_html(md_path)
    assert 'src="https://example.com/img.png"' in html


def test_missing_local_image_is_left_untouched(tmp_path: Path) -> None:
    md_path = tmp_path / "doc.md"
    md_path.write_text("![x](missing.png)\n", encoding="utf-8")

    html = convert_to_html(md_path)
    assert 'src="missing.png"' in html
    assert "data:image/png" not in html


def test_local_svg_is_embedded(tmp_path: Path) -> None:
    svg = '<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10"><rect width="10" height="10"/></svg>'
    (tmp_path / "icon.svg").write_text(svg, encoding="utf-8")

    md_path = tmp_path / "doc.md"
    md_path.write_text("![icon](icon.svg)\n", encoding="utf-8")

    html = convert_to_html(md_path)
    assert "data:image/svg+xml" in html


def test_custom_css_is_injected() -> None:
    html = convert_to_html(FIXTURES / "basic.md", css="body{color:red}")
    assert "body{color:red}" in html


def test_missing_file_raises() -> None:
    with pytest.raises(FileNotFoundError):
        convert_to_html(Path("does/not/exist.md"))
