# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-04-28

### Added

- Desktop GUI with drag & drop and file picker for `.md` / `.markdown` files
- Live HTML preview with full-document scroll support
- PDF export via headless Chromium (Playwright) — consistent rendering across Windows, macOS, and Linux
- Syntax highlighting for fenced code blocks (Pygments / Monokai theme)
- Support for images (base64-embedded), SVG, inline HTML, and LaTeX math
- Configurable page size: A4, A3, A5, Letter, Legal
- Custom CSS injection per export session
- Persisted settings across sessions (output directory, page size, custom CSS)
- PDF footer watermark with page numbers and author credit (`Developed by @costamagnus · v1.0.0`)
- CLI mode: convert `.md` files from the terminal with full option support
- Python API for programmatic use
- `--install-browser` command for one-time Chromium download (~150 MB)

[Unreleased]: https://github.com/matiascostamagna/md-to-pdf/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/matiascostamagna/md-to-pdf/releases/tag/v1.0.0
