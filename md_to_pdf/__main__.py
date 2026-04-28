"""MD → PDF Converter — entry point.

Usage:
    md-to-pdf input.md -o output.pdf          # CLI mode
    md-to-pdf --gui                            # GUI mode
    md-to-pdf input.md                         # Convert with auto output name
"""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from .css import load_default_css
from .gui import run_gui
from .renderer import ChromiumNotInstalledError, install_browser, md_to_pdf


def _cli() -> None:
    parser = argparse.ArgumentParser(
        prog="md-to-pdf",
        description="Convert Markdown files to PDF with full syntax support.",
    )
    parser.add_argument(
        "input",
        nargs="?",
        type=Path,
        help="Markdown file to convert",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=None,
        help="Output PDF path (default: input name with .pdf extension)",
    )
    parser.add_argument(
        "--css",
        type=Path,
        default=None,
        help="Custom CSS file to override default styles",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the graphical interface",
    )
    parser.add_argument(
        "--install-browser",
        action="store_true",
        help="Download the Chromium binary used for PDF rendering (~150 MB, one-time)",
    )
    parser.add_argument(
        "--title",
        type=str,
        default="",
        help="Document title (default: filename stem)",
    )
    parser.add_argument(
        "--page-size",
        type=str,
        default="A4",
        choices=["A4", "A3", "A5", "Letter", "Legal"],
        help="Page size (default: A4)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    if args.install_browser:
        sys.exit(install_browser())

    if args.gui:
        run_gui()
        return

    if not args.input:
        run_gui()
        return

    md_path: Path = args.input
    if not md_path.is_file():
        print(f"Error: file not found → {md_path}", file=sys.stderr)
        sys.exit(1)

    output_path: Path = args.output or md_path.with_suffix(".pdf")

    css_content = load_default_css()
    if args.css:
        css_path: Path = args.css
        if css_path.is_file():
            css_content = css_path.read_text(encoding="utf-8")
        else:
            print(f"Warning: CSS file not found → {css_path}, using defaults", file=sys.stderr)

    title = args.title or md_path.stem

    try:
        result = md_to_pdf(
            md_path,
            output_path,
            css_content=css_content,
            title=title,
            page_size=args.page_size,
        )
        print(f"PDF generated → {result}")
    except ChromiumNotInstalledError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
    except Exception as exc:
        print(f"Error generating PDF: {exc}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    _cli()


if __name__ == "__main__":
    main()