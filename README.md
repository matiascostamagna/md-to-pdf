# 📄 MD → PDF

[![CI](https://github.com/matiascostamagna/md-to-pdf/actions/workflows/ci.yml/badge.svg)](https://github.com/matiascostamagna/md-to-pdf/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

> Convert Markdown to polished PDFs — CLI, desktop GUI, or Python API.

Powered by **Playwright** (Chromium headless) for PDF generation and **pywebview** for the optional desktop GUI.

---

## ⚠️ Important Note (Linux users)

The CLI works out-of-the-box using Playwright (no system GUI dependencies required).

However, the *desktop GUI requires a system GUI backend (Qt or GTK)* on Linux.

If the GUI fails to start, you likely need to install additional system libraries.

---

## ✨ Features

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

## 📦 Installation

### Recommended (isolated environment)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```
---

### Alternative (recommended for CLI tools)

```bash
pipx install .
```

---

### 🌐 Install browser (required)

This project uses Playwright to download Chromium:

```bash
md-to-pdf --install-browser
```
Browser binaries are cached by Playwright in:
- Linux/macOS: `~/.cache/ms-playwright`
- Windows: `%LOCALAPPDATA%\ms-playwright`

### 🐧 Linux system dependencies

Playwright requires system libraries for Chromium:

```bash
sudo apt update && sudo apt install -y \
  libatk1.0-0 libatk-bridge2.0-0 libcups2 libdbus-1-3 libexpat1 libgbm1 \
  libpango-1.0-0 libpangocairo-1.0-0 libx11-6 libx11-xcb1 libxcb1 \
  libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 \
  libxinerama1 libxrandr2 libxrender1 libxss1 libxtst6 libxkbcommon0
```

Then:

```bash
pip install -e .
md-to-pdf --install-browser
```

---

#### 🖥️ GUI dependencies (Linux only)

The GUI uses **pywebview**, which requires a native backend.

#### Option A — Qt (recommended)

```bash
pip install pyqt6 PyQt6-WebEngine qtpy
sudo apt install libxcb-cursor0
```

#### Option B — GTK (alternative)

```bash
sudo apt install python3-gi gir1.2-gtk-3.0
pip install PyGObject
```

#### 🔧 If GUI fails to start

Force Qt backend:

```bash
PYWEBVIEW_GUI=qt md-to-pdf
```

---

## 🚀 Usage

### GUI mode

```bash
md-to-pdf
```

or

```bash
md-to-pdf --gui
```

Drop a `.md` file onto the window (or click **Open**), adjust settings in the sidebar,
and click **Convert to PDF**. Output directory, page size, and custom CSS are remembered
between sessions.

### CLI mode

```bash
md-to-pdf document.md                        # output: document.pdf (same dir)
```
```bash
md-to-pdf document.md -o ~/exports/out.pdf
```
```bash
md-to-pdf document.md --page-size Letter
```
```bash
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

### 🐍 Python API

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

## 🧱 Project Structure

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

## 🛠️ Development

```sh
pip install -e ".[dev]"
pytest
ruff check . 
```

## 📌 Notes
- CLI mode uses Playwright only
- GUI mode requires Qt or GTK on Linux
- Windows/macOS generally work without extra system packages
- Qt is preferred if multiple GUI backends are installed
- If GUI fails, force backend with PYWEBVIEW_GUI=qt

---

## License

MIT
