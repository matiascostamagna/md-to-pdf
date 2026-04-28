"""
Markdown to PDF converter — core engine.

Converts Markdown to HTML using Python-Markdown with PyMdown extensions,
supporting: code blocks (syntax highlighted), images (local + remote),
SVG inline, embedded HTML, LaTeX math formulas, tables, footnotes,
definition lists, abbreviations, emoji, task lists, admonitions,
and anchors.
"""

from __future__ import annotations

import base64
import mimetypes
import re
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlparse

import markdown
from pygments.formatters import HtmlFormatter
from pymdownx import emoji as _pymdownx_emoji

EXTENSIONS = [
    "markdown.extensions.tables",
    "markdown.extensions.footnotes",
    "markdown.extensions.def_list",
    "markdown.extensions.abbr",
    "markdown.extensions.attr_list",
    "markdown.extensions.md_in_html",
    "markdown.extensions.toc",
    "markdown.extensions.codehilite",
    "markdown.extensions.fenced_code",
    "markdown.extensions.smarty",
    "pymdownx.superfences",
    "pymdownx.highlight",
    "pymdownx.inlinehilite",
    "pymdownx.magiclink",
    "pymdownx.tilde",
    "pymdownx.caret",
    "pymdownx.mark",
    "pymdownx.tasklist",
    "pymdownx.emoji",
    "pymdownx.details",
    "pymdownx.arithmatex",
    "pymdownx.keys",
    "pymdownx.smartsymbols",
    "pymdownx.snippets",
]


EXTENSION_CONFIGS: dict[str, dict[str, Any]] = {
    "pymdownx.highlight": {
        "linenums": True,
        "linenums_style": "table",
        "guess_lang": True,
        "css_class": "highlight",
    },
    "pymdownx.superfences": {
        "custom_fences": [
            {
                "name": "mermaid",
                "class": "mermaid",
                "format": "pymdownx.superfences.fence_div_format",
            }
        ]
    },
    "pymdownx.emoji": {
        "emoji_index": _pymdownx_emoji.twemoji,
        "emoji_generator": _pymdownx_emoji.to_alt,
    },
    "pymdownx.magiclink": {
        "repo_url_shortener": True,
        "repo_url_shorthand": True,
        "social_url_shorthand": True,
        "provider": "github",
    },
    "pymdownx.tasklist": {
        "custom_checkbox": True,
        "clickable_checkbox": True,
    },
    "markdown.extensions.codehilite": {
        "linenums": False,
        "guess_lang": True,
    },
    "pymdownx.arithmatex": {
        "generic": True,
    },
}


PYGMENTS_CSS = ""


def _ensure_pygments_css() -> str:
    global PYGMENTS_CSS
    if not PYGMENTS_CSS:
        formatter = HtmlFormatter(style="monokai", linenos="table")
        css_lines = formatter.get_style_defs(".highlight")
        PYGMENTS_CSS = f"<style>{css_lines}</style>"
    return PYGMENTS_CSS


def _image_to_data_uri(path: Path) -> str:
    mime, _ = mimetypes.guess_type(path.name)
    mime = mime or "image/png"
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{data}"


def _embed_local_images(html: str, base_path: Path) -> str:
    def _replace_img(match: re.Match[str]) -> str:
        src = match.group("src")
        parsed = urlparse(src)
        if parsed.scheme and parsed.scheme not in ("file", ""):
            return match.group(0)
        clean = src.split("?")[0].split("#")[0]
        img_path = base_path / clean
        if img_path.is_file():
            data_uri = _image_to_data_uri(img_path)
            return match.group(0).replace(f'src="{src}"', f'src="{data_uri}"')
        if "/" in clean or "\\" in clean:
            alt_path = Path(clean)
            if alt_path.is_file():
                data_uri = _image_to_data_uri(alt_path)
                return match.group(0).replace(f'src="{src}"', f'src="{data_uri}"')
        return match.group(0)

    return re.sub(
        r'<img[^>]+src="(?P<src>[^"]+)"',
        _replace_img,
        html,
    )


def _embed_local_svg(html: str, base_path: Path) -> str:
    def _replace_svg(match: re.Match[str]) -> str:
        src = match.group("src")
        parsed = urlparse(src)
        if parsed.scheme and parsed.scheme not in ("file", ""):
            return match.group(0)
        clean = src.split("?")[0].split("#")[0]
        svg_path = base_path / clean
        if not svg_path.is_file() and ("/" in clean or "\\" in clean):
            svg_path = Path(clean)
        if svg_path.is_file() and svg_path.suffix.lower() == ".svg":
            svg_content = svg_path.read_text(encoding="utf-8")
            data_uri = f"data:image/svg+xml;charset=utf-8,{quote(svg_content)}"
            return match.group(0).replace(f'src="{src}"', f'src="{data_uri}"')
        return match.group(0)

    return re.sub(
        r'<img[^>]+src="(?P<src>[^"]+\.svg)"',
        _replace_svg,
        html,
    )


_PAGE_BREAK_RE = re.compile(r"\\newpage\s*", re.IGNORECASE)


def _inject_page_breaks(html: str) -> str:
    return _PAGE_BREAK_RE.sub('<div class="page-break"></div>', html)


def _wrap_html(body: str, *, title: str = "Document", css: str = "") -> str:
    pygments_css = _ensure_pygments_css()
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
{pygments_css}
<style>{css}</style>
</head>
<body>
<article class="markdown-body">
{body}
</article>
</body>
</html>"""


def convert_to_html(md_path: Path, *, css: str = "", title: str = "") -> str:
    md_source = md_path.read_text(encoding="utf-8")
    base_path = md_path.resolve().parent

    md = markdown.Markdown(
        extensions=EXTENSIONS,
        extension_configs=EXTENSION_CONFIGS,
    )
    body = md.convert(md_source)

    body = _embed_local_images(body, base_path)
    body = _embed_local_svg(body, base_path)
    body = _inject_page_breaks(body)

    return _wrap_html(body, title=title or md_path.stem, css=css)