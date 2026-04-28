"""Default CSS for PDF rendering — inspired by GitHub Markdown style."""

DEFAULT_CSS = r"""
@page {
  size: A4;
  margin: 2.2cm 2cm 2.4cm 2cm;
  @bottom-center {
    content: counter(page);
    font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
    font-size: 9pt;
    color: #6b7280;
  }
}

@page :first {
  @bottom-center {
    content: none;
  }
}

* {
  box-sizing: border-box;
}

html {
  font-size: 11pt;
  font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
  line-height: 1.65;
  color: #1f2937;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}

.markdown-body {
  max-width: 100%;
}

/* ===================== HEADINGS ===================== */

h1 {
  font-size: 2em;
  font-weight: 700;
  margin: 0 0 0.5em 0;
  padding-bottom: 0.3em;
  border-bottom: 2px solid #e5e7eb;
  color: #111827;
  page-break-after: avoid;
}

h2 {
  font-size: 1.55em;
  font-weight: 600;
  margin: 1.6em 0 0.5em 0;
  padding-bottom: 0.25em;
  border-bottom: 1px solid #e5e7eb;
  color: #1f2937;
  page-break-after: avoid;
}

h3 {
  font-size: 1.3em;
  font-weight: 600;
  margin: 1.4em 0 0.4em 0;
  color: #374151;
  page-break-after: avoid;
}

h4 {
  font-size: 1.15em;
  font-weight: 600;
  margin: 1.2em 0 0.3em 0;
  color: #4b5563;
  page-break-after: avoid;
}

h5, h6 {
  font-size: 1em;
  font-weight: 600;
  margin: 1em 0 0.2em 0;
  color: #6b7280;
  page-break-after: avoid;
}

/* ===================== PARAGRAPHS & TEXT ===================== */

p {
  margin: 0 0 0.8em 0;
  text-align: justify;
  orphans: 3;
  widows: 3;
}

strong { font-weight: 600; color: #111827; }
em { font-style: italic; }
del { color: #9ca3af; text-decoration: line-through; }
mark { background: #fef08a; padding: 0.1em 0.3em; border-radius: 3px; }

a { color: #3b82f6; text-decoration: underline; }
a:visited { color: #7c3aed; }

hr {
  border: none;
  border-top: 1.5px solid #d1d5db;
  margin: 2em 0;
}

/* ===================== LISTS ===================== */

ul, ol {
  margin: 0 0 0.8em 0;
  padding-left: 1.8em;
}

li { margin-bottom: 0.25em; }

ul { list-style-type: disc; }
ul ul { list-style-type: circle; }
ul ul ul { list-style-type: square; }

ol { list-style-type: decimal; }

li > p { margin: 0.3em 0; }

.task-list {
  list-style: none;
  padding-left: 0.5em;
}

.task-list-item {
  list-style: none;
}

.task-list-item input[type="checkbox"] {
  margin-right: 0.5em;
}

/* ===================== CODE ===================== */

code {
  font-family: "Cascadia Code", "Fira Code", "JetBrains Mono", "Consolas", monospace;
  font-size: 0.9em;
  background: #f3f4f6;
  padding: 0.18em 0.4em;
  border-radius: 4px;
  color: #be123c;
  white-space: pre-wrap;
  word-break: break-word;
}

pre {
  background: #1e1e2e;
  color: #cdd6f4;
  border: 1px solid #313244;
  border-radius: 8px;
  padding: 1em 1.2em;
  margin: 1em 0;
  overflow-x: auto;
  white-space: pre;
  font-size: 9pt;
  line-height: 1.55;
  page-break-inside: avoid;
}

pre code {
  background: none;
  color: inherit;
  padding: 0;
  border-radius: 0;
  font-size: inherit;
}

.highlighttable {
  width: 100%;
  border-collapse: collapse;
}

.highlighttable td.linenos {
  color: #6c7086;
  background: #181825;
  padding: 0.5em 0.8em;
  text-align: right;
  user-select: none;
  border-right: 1px solid #313244;
  width: 1%;
  white-space: nowrap;
}

.highlighttable td.code {
  padding: 0.5em 1em;
  width: 99%;
}

/* ===================== BLOCKQUOTES ===================== */

blockquote {
  margin: 1em 0;
  padding: 0.6em 1.2em;
  border-left: 4px solid #93c5fd;
  background: #eff6ff;
  color: #374151;
  border-radius: 0 6px 6px 0;
  page-break-inside: avoid;
}

blockquote p:last-child { margin-bottom: 0; }

/* ===================== TABLES ===================== */

table {
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0;
  font-size: 9.5pt;
  page-break-inside: avoid;
}

thead {
  background: #f9fafb;
  border-bottom: 2px solid #d1d5db;
}

th {
  padding: 0.55em 0.9em;
  text-align: left;
  font-weight: 600;
  color: #374151;
  white-space: nowrap;
}

td {
  padding: 0.45em 0.9em;
  border-bottom: 1px solid #e5e7eb;
  vertical-align: top;
}

tr:nth-child(even) td {
  background: #f9fafb;
}

/* ===================== IMAGES ===================== */

img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 1em auto;
  border-radius: 6px;
  page-break-inside: avoid;
}

figure {
  margin: 1.2em 0;
  text-align: center;
  page-break-inside: avoid;
}

figcaption {
  font-size: 9pt;
  color: #6b7280;
  margin-top: 0.4em;
}

/* ===================== ADMONITIONS / DETAILS ===================== */

details {
  margin: 1em 0;
  padding: 0.8em 1.2em;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: #f9fafb;
  page-break-inside: avoid;
}

details[open] summary {
  margin-bottom: 0.5em;
}

summary {
  cursor: pointer;
  font-weight: 600;
  color: #374151;
  padding: 0.2em 0;
}

.admonition {
  margin: 1em 0;
  padding: 0.8em 1.2em;
  border-left: 4px solid;
  border-radius: 0 8px 8px 0;
  page-break-inside: avoid;
}

.admonition.info,
.admonition.note {
  border-color: #3b82f6;
  background: #eff6ff;
}

.admonition.warning {
  border-color: #f59e0b;
  background: #fffbeb;
}

.admonition.danger,
.admonition.error {
  border-color: #ef4444;
  background: #fef2f2;
}

.admonition.success,
.admonition.tip {
  border-color: #10b981;
  background: #ecfdf5;
}

/* ===================== FOOTNOTES ===================== */

.footnote {
  font-size: 9pt;
  color: #6b7280;
}

.footnotes {
  margin-top: 2em;
  padding-top: 1em;
  border-top: 1px solid #d1d5db;
  font-size: 9pt;
}

.footnotes ol { padding-left: 1.5em; }

.footnotes li { margin-bottom: 0.3em; }

/* ===================== TABLE OF CONTENTS ===================== */

.toc {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 1em 1.5em;
  margin: 1em 0;
  page-break-after: always;
}

.toc ul {
  list-style: none;
  padding-left: 0;
}

.toc li {
  margin-bottom: 0.35em;
}

.toc a {
  color: #374151;
  text-decoration: none;
}

.toc a::after {
  content: target-counter(attr(href), page);
  float: right;
  color: #9ca3af;
}

/* ===================== DEFINITION LISTS ===================== */

dl { margin: 1em 0; }
dt { font-weight: 600; color: #374151; margin-top: 0.6em; }
dd { margin-left: 1.5em; margin-bottom: 0.5em; color: #4b5563; }

/* ===================== KEYBOARD KEYS ===================== */

kbd {
  display: inline-block;
  padding: 0.15em 0.45em;
  font-size: 0.85em;
  font-family: "Cascadia Code", "Fira Code", "Consolas", monospace;
  background: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  box-shadow: 0 1px 0 #d1d5db;
  color: #374151;
}

/* ===================== MATH ===================== */

.math {
  overflow-x: auto;
  page-break-inside: avoid;
}

/* ===================== PAGE BREAKS ===================== */

.page-break {
  page-break-after: always;
  visibility: hidden;
  height: 0;
  margin: 0;
  padding: 0;
}

/* ===================== COVER PAGE ===================== */

.cover-page {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  text-align: center;
  page-break-after: always;
}

.cover-page h1 {
  font-size: 2.5em;
  border-bottom: none;
  margin-bottom: 0.3em;
}

.cover-page .subtitle {
  font-size: 1.2em;
  color: #6b7280;
  margin-bottom: 2em;
}

.cover-page .date {
  font-size: 0.9em;
  color: #9ca3af;
}

/* ===================== PRINT OPTIMIZATIONS ===================== */

h1, h2, h3, h4, h5, h6,
pre, blockquote, table, img, figure,
.admonition, details, .math {
  page-break-inside: avoid;
}

h1, h2, h3, h4 {
  page-break-after: avoid;
}
"""


def load_default_css() -> str:
    return DEFAULT_CSS