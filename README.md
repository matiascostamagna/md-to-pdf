# MD → PDF Converter

Convert Markdown files to PDF with full support for:

- **Text** — headings, paragraphs, bold, italic, strikethrough, highlighted
- **Code** — fenced code blocks with syntax highlighting (Pygments, Monokai theme)
- **Images** — local images auto-embedded as base64 data URIs
- **SVG** — inline SVG rendering and embedded SVG files
- **HTML** — raw HTML blocks rendered directly
- **Math** — LaTeX math formulas via Arithmatex + MathJax
- **Tables** — GitHub-style tables with alternating rows
- **Lists** — ordered, unordered, task lists with checkboxes
- **Blockquotes, Footnotes, Definition Lists, Abbreviations**
- **Admonitions** — info, warning, danger, success callouts
- **Mermaid diagrams** — rendered as divs
- **Emoji** — twemoji support
- **Table of Contents** — auto-generated
- **Keyboard keys** — `<kbd>` styling
- **Page breaks** — `\newpage` command

## Installation

### Windows / macOS

```
pip install -e .
md-to-pdf --install-browser
```

### Linux

On Linux, Playwright needs a few system libraries. Then same steps:

```
# Ubuntu / Debian
sudo apt update
sudo apt install libatk1.0-0 libatk-bridge2.0-0 libcups2 libdbus-1-3 \
  libexpat1 libgbm1 libpango-1.0-0 libpangocairo-1.0-0 libx11-6 libx11-xcb1 \
  libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 \
  libxi6 libxinerama1 libxrandr2 libxrender1 libxss1 libxtst6 libxkbcommon0

# Fedora / RHEL
sudo dnf install atk at-spi2-atk cups dbus expat libgbm libpango libx11 \
  libxcomposite libxcursor libxdamage libxext libxfixes libxi libxinerama \
  libxrandr libxrender libxss libxtst libxkbcommon

# Arch
sudo pacman -S atk at-spi2-atk cups dbus expat libgbm pango libx11 \
  libxcomposite libxcursor libxdamage libxext libxfixes libxi libxinerama \
  libxrandr libxrender libxss libxtst libxkbcommon
```

Then:

```
pip install -e .
md-to-pdf --install-browser
```

### How it works

The first command installs Python deps. The second downloads the Chromium
binary used for PDF rendering (~150 MB, one-time, cached under
`%LOCALAPPDATA%/ms-playwright` on Windows / `~/.cache/ms-playwright` on
Linux/macOS).

PDF rendering uses **Playwright** (Chromium headless) — same engine on every
OS, full CSS3 + JavaScript support, all dependencies managed by `pip`.

## Usage

### GUI

```
md-to-pdf --gui
# or simply
md-to-pdf
```

Drag-and-drop `.md` files, preview them, configure output settings, and export to PDF.

### CLI

```
md-to-pdf document.md
md-to-pdf document.md -o output.pdf
md-to-pdf document.md --css custom.css --title "My Document"
md-to-pdf document.md --page-size Letter
```

### Options

| Flag | Description |
|------|-------------|
| `-o, --output` | Output PDF path |
| `--css` | Custom CSS file |
| `--title` | Document title |
| `--page-size` | A4 / A3 / A5 / Letter / Legal (default: A4) |
| `--gui` | Launch GUI |
| `--install-browser` | Download Chromium (~150 MB, one-time) |
| `-v, --verbose` | Verbose logging |

## Project Structure

```
md_to_pdf/
├── __init__.py       # Package marker
├── __main__.py       # Entry point (CLI + GUI dispatch)
├── converter.py      # Markdown → HTML engine
├── renderer.py       # HTML → PDF via Playwright (Chromium headless)
├── settings.py       # Persistent GUI preferences
├── css.py            # Default PDF CSS stylesheet
├── gui.py            # pywebview desktop GUI
└── assets/           # Static assets (future)
```