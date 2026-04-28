# MD → PDF

[![CI](https://github.com/matiascostamagna/md-to-pdf/actions/workflows/ci.yml/badge.svg)](https://github.com/matiascostamagna/md-to-pdf/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

> Convert Markdown to polished PDFs — CLI, desktop GUI, or Python API.

Powered by **Playwright** (Chromium headless): same render engine on Windows,
macOS, and Linux; all dependencies managed by `pip`, no system binaries required.

---

## Features

| Category | What's supported |
|----------|-----------------|
| Text | Headings, bold, italic, strikethrough, highlight, superscript, subscript |
| Code | Fenced blocks with syntax highlighting (Monokai), inline code, line numbers |
| Images | Local files auto-embedded as base64 · SVG inline rendering |
| Math | LaTeX via Arithmatex (`$...$` / `$$...$$`) |
| Tables | GitHub-style with alternating rows |
| Lists | Ordered · unordered · task lists with checkboxes |
| Callouts | Blockquotes · admonitions (info / warning / danger / tip) · `<details>` |
| Diagrams | Mermaid (rendered by Chromium at export time) |
| Structure | Table of contents · footnotes · definition lists · abbreviations · `\newpage` |
| Extras | Emoji · keyboard keys (`<kbd>`) · magic links · smart symbols |

---

## Installation

### Windows / macOS

```sh
pip install -e .
md-to-pdf --install-browser   # one-time Chromium download (~150 MB)
```

### Linux

Playwright's Chromium build requires a few system libs:

```sh
# Ubuntu / Debian
sudo apt update && sudo apt install -y \
  libatk1.0-0 libatk-bridge2.0-0 libcups2 libdbus-1-3 libexpat1 libgbm1 \
  libpango-1.0-0 libpangocairo-1.0-0 libx11-6 libx11-xcb1 libxcb1 \
  libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 \
  libxinerama1 libxrandr2 libxrender1 libxss1 libxtst6 libxkbcommon0

# Fedora / RHEL
sudo dnf install -y atk at-spi2-atk cups dbus expat libgbm libpango libx11 \
  libxcomposite libxcursor libxdamage libxext libxfixes libxi libxinerama \
  libxrandr libxrender libxss libxtst libxkbcommon

# Arch
sudo pacman -S --needed atk at-spi2-atk cups dbus expat libgbm pango libx11 \
  libxcomposite libxcursor libxdamage libxext libxfixes libxi libxinerama \
  libxrandr libxrender libxss libxtst libxkbcommon
```

Then:

```sh
pip install -e .
md-to-pdf --install-browser
```

The browser binary is cached by Playwright at `~/.cache/ms-playwright` (Linux/macOS)
or `%LOCALAPPDATA%\ms-playwright` (Windows) — not inside this project.

---

## Usage

### GUI

```sh
md-to-pdf          # launches the GUI
md-to-pdf --gui
```

Drop a `.md` file onto the window (or click **Open**), adjust settings in the sidebar,
and click **Convert to PDF**. Output directory, page size, and custom CSS are remembered
between sessions.

### CLI

```sh
md-to-pdf document.md                        # output: document.pdf (same dir)
md-to-pdf document.md -o ~/exports/out.pdf
md-to-pdf document.md --page-size Letter
md-to-pdf document.md --css custom.css --title "My Report"
```

### CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `-o, --output` | `<input>.pdf` | Output path |
| `--page-size` | `A4` | `A4` · `A3` · `A5` · `Letter` · `Legal` |
| `--css` | built-in | Path to a CSS file to override styles |
| `--title` | filename stem | PDF document title |
| `--gui` | — | Launch the desktop GUI |
| `--install-browser` | — | Download Chromium (run once after install) |
| `-v, --verbose` | — | Verbose logging |

### Python API

```python
from pathlib import Path
from md_to_pdf.renderer import md_to_pdf
from md_to_pdf.css import load_default_css

md_to_pdf(
    Path("document.md"),
    Path("output.pdf"),
    css_content=load_default_css(),
    title="My Document",
    page_size="A4",
)
```

---

## Project Structure

```
md_to_pdf/
├── __main__.py   — CLI entry point + GUI dispatch
├── converter.py  — Markdown → HTML (python-markdown + pymdownx)
├── renderer.py   — HTML → PDF via Playwright (Chromium headless)
├── css.py        — Default print stylesheet (GitHub-inspired)
├── settings.py   — Persistent GUI preferences (JSON, per-OS config dir)
└── gui.py        — Desktop GUI (pywebview)

tests/
├── fixtures/     — Sample .md files for testing
├── test_converter.py
├── test_renderer.py
└── test_settings.py
```

---

## Development

```sh
pip install -e ".[dev]"
pytest
```

Dev extras: `ruff` (linter) · `pytest`.

---

## License

MIT
