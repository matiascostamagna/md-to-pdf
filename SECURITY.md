# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.x   | ✅        |

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Send a report to **matias.costamagna@mi.unc.edu.ar** with:
- A description of the vulnerability
- Steps to reproduce
- Potential impact

You can expect:
- Acknowledgement within **48 hours**
- A patch or mitigation within **14 days** for confirmed issues

## Scope

Issues considered in scope:
- Path traversal via Markdown file or output path inputs
- Arbitrary code execution triggered by crafted Markdown or CSS
- Sensitive data exposure through the PDF generation pipeline (Playwright/Chromium)

Out of scope:
- Vulnerabilities in upstream dependencies (Playwright, pywebview, python-markdown)
- Social engineering attacks
