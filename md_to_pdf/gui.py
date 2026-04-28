"""GUI application for MD to PDF converter — built with pywebview."""

from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import webview

from .converter import convert_to_html
from .css import load_default_css
from .renderer import ChromiumNotInstalledError, install_browser, md_to_pdf
from .settings import load_settings, save_settings

logger = logging.getLogger(__name__)

GUI_HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MD → PDF Converter</title>
<style>
:root {
  --bg: #0f172a;
  --surface: #1e293b;
  --border: #334155;
  --text: #e2e8f0;
  --muted: #94a3b8;
  --accent: #3b82f6;
  --accent-hover: #60a5fa;
  --danger: #ef4444;
  --success: #22c55e;
  --radius: 10px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
  background: var(--bg);
  color: var(--text);
  user-select: none;
  -webkit-user-select: none;
  overflow: hidden;
  height: 100vh;
}

.container {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

/* ---- TOOLBAR ---- */
.toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  flex-shrink: 0;
  -webkit-app-region: drag;
}

.toolbar button,
.toolbar label {
  -webkit-app-region: no-drag;
}

.app-title {
  font-size: 15px;
  font-weight: 700;
  letter-spacing: -0.3px;
  margin-right: auto;
  display: flex;
  align-items: center;
  gap: 8px;
}

.app-title .icon { font-size: 20px; }

.btn {
  padding: 8px 18px;
  border: none;
  border-radius: var(--radius);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
  font-family: inherit;
}

.btn-primary {
  background: var(--accent);
  color: white;
}
.btn-primary:hover { background: var(--accent-hover); }
.btn-primary:disabled {
  background: var(--border);
  color: var(--muted);
  cursor: not-allowed;
}

.btn-outline {
  background: transparent;
  color: var(--accent);
  border: 1.5px solid var(--accent);
}
.btn-outline:hover { background: rgba(59,130,246,0.1); }

.btn-danger {
  background: transparent;
  color: var(--danger);
  border: 1.5px solid var(--danger);
}
.btn-danger:hover { background: rgba(239,68,68,0.1); }

/* ---- MAIN CONTENT ---- */
.main {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* ---- PREVIEW PANE ---- */
.preview {
  flex: 1;
  display: flex;
  align-items: flex-start;
  justify-content: flex-start;
  overflow-y: auto;
  background: #f8fafc;
  position: relative;
}

.preview iframe {
  width: 100%;
  border: none;
}

/* ---- DROP ZONE ---- */
.drop-zone {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  position: absolute;
  inset: 0;
}

.drop-zone.hidden { display: none; }

.drop-icon {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  background: var(--surface);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  border: 2px dashed var(--border);
}

.drop-text { text-align: center; }

.drop-text .primary {
  font-size: 16px;
  font-weight: 600;
  color: var(--text);
}

.drop-text .secondary {
  font-size: 13px;
  color: var(--muted);
  margin-top: 4px;
}

/* ---- SIDEBAR ---- */
.sidebar {
  width: 280px;
  background: var(--surface);
  border-left: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  overflow-y: auto;
}

.sidebar-section {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
}

.sidebar-title {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--muted);
  margin-bottom: 12px;
}

.field { margin-bottom: 12px; }

.field label {
  display: block;
  font-size: 12px;
  font-weight: 500;
  color: var(--muted);
  margin-bottom: 4px;
}

.field input,
.field select,
.field textarea {
  width: 100%;
  padding: 8px 10px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text);
  font-family: inherit;
  font-size: 13px;
  outline: none;
}

.field input:focus,
.field select:focus,
.field textarea:focus {
  border-color: var(--accent);
}

.field textarea {
  resize: vertical;
  min-height: 80px;
  font-family: "Cascadia Code", "Consolas", monospace;
  font-size: 11px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
  font-size: 12px;
}

.info-row .label { color: var(--muted); }
.info-row .value { font-weight: 500; }

/* ---- STATUS BAR ---- */
.status {
  padding: 8px 20px;
  background: var(--surface);
  border-top: 1px solid var(--border);
  font-size: 12px;
  color: var(--muted);
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.status .indicator {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--muted);
  flex-shrink: 0;
}

.status .indicator.ready { background: var(--success); }
.status .indicator.working { background: #f59e0b; animation: pulse 1s infinite; }
.status .indicator.error { background: var(--danger); }

@keyframes pulse {
  50% { opacity: 0.4; }
}

/* ---- TOAST ---- */
.toast {
  position: fixed;
  bottom: 50px;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px 24px;
  border-radius: var(--radius);
  font-size: 13px;
  font-weight: 500;
  z-index: 100;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s;
}

.toast.show { opacity: 1; }
.toast.success { background: #065f46; color: #6ee7b7; }
.toast.error { background: #7f1d1d; color: #fca5a5; }

/* Scrollbar */
.sidebar::-webkit-scrollbar { width: 5px; }
.sidebar::-webkit-scrollbar-track { background: transparent; }
.sidebar::-webkit-scrollbar-thumb { background: var(--border); border-radius: 10px; }
</style>
</head>
<body>
<div class="container">
  <div class="toolbar">
    <div class="app-title">
      <span class="icon">📄</span> MD → PDF
    </div>
    <button class="btn btn-outline" id="btn-open" title="Open Markdown file (Ctrl+O)">Open</button>
    <button class="btn btn-primary" id="btn-convert" disabled>Convert to PDF</button>
  </div>

  <div class="main">
    <div class="preview" id="preview-pane"
         ondragover="event.preventDefault(); this.classList.add('drag-over')"
         ondragleave="this.classList.remove('drag-over')"
         ondrop="handleDrop(event)">
      <div class="drop-zone" id="drop-zone">
        <div class="drop-icon">📥</div>
        <div class="drop-text">
          <div class="primary">Drop a Markdown file here</div>
          <div class="secondary">or click Open to browse</div>
        </div>
      </div>
      <iframe id="preview-frame" hidden></iframe>
    </div>

    <div class="sidebar" id="sidebar">
      <div class="sidebar-section">
        <div class="sidebar-title">File Info</div>
        <div class="info-row">
          <span class="label">Name</span>
          <span class="value" id="info-name">—</span>
        </div>
        <div class="info-row">
          <span class="label">Size</span>
          <span class="value" id="info-size">—</span>
        </div>
        <div class="info-row">
          <span class="label">Lines</span>
          <span class="value" id="info-lines">—</span>
        </div>
      </div>

      <div class="sidebar-section">
        <div class="sidebar-title">Export Settings</div>
        <div class="field">
          <label for="output-dir">Output Directory</label>
          <input type="text" id="output-dir" placeholder="Same as source">
        </div>
        <button class="btn btn-outline" id="btn-output-dir" style="width:100%; margin-bottom:12px;">Choose Directory</button>
        <div class="field">
          <label for="page-size">Page Size</label>
          <select id="page-size">
            <option value="A4" selected>A4</option>
            <option value="Letter">Letter</option>
            <option value="Legal">Legal</option>
            <option value="A3">A3</option>
            <option value="A5">A5</option>
          </select>
        </div>
        <div class="field">
          <label for="custom-css">Custom CSS</label>
          <textarea id="custom-css" placeholder="Override default styles..."></textarea>
        </div>
      </div>
    </div>
  </div>

  <div class="status">
    <span class="indicator" id="status-indicator"></span>
    <span id="status-text">Ready</span>
  </div>

  <div class="toast" id="toast"></div>
</div>

<script>
const dropZone = document.getElementById('drop-zone');
const previewFrame = document.getElementById('preview-frame');
const btnConvert = document.getElementById('btn-convert');
const btnOpen = document.getElementById('btn-open');
const statusText = document.getElementById('status-text');
const statusIndicator = document.getElementById('status-indicator');
const toast = document.getElementById('toast');

let currentMdPath = null;

// ────────────────────────────────────
// LOAD PERSISTED SETTINGS
// ────────────────────────────────────

window.addEventListener('pywebviewready', function() {
  pywebview.api.load_settings().then(function(s) {
    if (s.output_dir) document.getElementById('output-dir').value = s.output_dir;
    if (s.page_size) document.getElementById('page-size').value = s.page_size;
    if (s.custom_css) document.getElementById('custom-css').value = s.custom_css;
  });
});

// ────────────────────────────────────
// FILE OPEN
// ────────────────────────────────────

btnOpen.addEventListener('click', () => {
  pywebview.api.choose_file().then(function(filePath) {
    if (filePath) loadFile(filePath);
  }).catch(handleError);
});

// ────────────────────────────────────
// DRAG & DROP
// ────────────────────────────────────

window.handleDrop = function(event) {
  event.preventDefault();
  event.target.classList.remove('drag-over');
  const files = event.dataTransfer.files;
  if (files.length === 0) return;
  const f = files[0];
  if (f.path) {
    loadFile(f.path);
    return;
  }
  // Fallback: pywebview build doesn't expose .path. Read the blob and ship
  // contents + filename to Python, which writes them to a temp file.
  const reader = new FileReader();
  reader.onload = function() {
    pywebview.api.load_file_from_content(f.name, reader.result)
      .then(handleLoaded).catch(handleError);
  };
  reader.onerror = function() { showToast('Could not read dropped file', 'error'); };
  reader.readAsText(f);
};

// ────────────────────────────────────
// LOAD FILE
// ────────────────────────────────────

function loadFile(filePath) {
  currentMdPath = filePath;
  setStatus('working', 'Loading preview...');
  pywebview.api.load_file(filePath).then(handleLoaded).catch(handleError);
}

function handleLoaded(info) {
  currentMdPath = info.path;
  document.getElementById('info-name').textContent = info.name;
  document.getElementById('info-size').textContent = info.size;
  document.getElementById('info-lines').textContent = String(info.lines);
  document.title = info.name + ' — MD → PDF';

  dropZone.classList.add('hidden');
  previewFrame.hidden = false;

  previewFrame.style.height = '100%';
  previewFrame.srcdoc = info.preview_html;
  previewFrame.onload = function() {
    const iframeDoc = previewFrame.contentDocument || previewFrame.contentWindow.document;
    setTimeout(() => {
      const body = iframeDoc.body;
      const html = iframeDoc.documentElement;
      const h = Math.max(body.scrollHeight, html.scrollHeight, body.offsetHeight, html.offsetHeight);
      previewFrame.style.height = h + 'px';
    }, 150);
  };

  btnConvert.disabled = false;
  setStatus('ready', 'Ready — ' + (info.path || 'File loaded'));
  showToast('File loaded successfully', 'success');
}

// ────────────────────────────────────
// CONVERT
// ────────────────────────────────────

btnConvert.addEventListener('click', () => {
  if (!currentMdPath) return;
  setStatus('working', 'Converting to PDF...');
  btnConvert.disabled = true;

  const settings = {
    output_dir: document.getElementById('output-dir').value,
    page_size: document.getElementById('page-size').value,
    custom_css: document.getElementById('custom-css').value,
  };

  pywebview.api.convert(currentMdPath, JSON.stringify(settings)).then(handleConverted).catch(handleError);
  pywebview.api.save_settings(JSON.stringify(settings));
});

function handleConverted(result) {
  btnConvert.disabled = false;
  if (result.success) {
    setStatus('ready', 'PDF saved → ' + result.output);
    showToast('PDF generated successfully!', 'success');
    pywebview.api.open_output(result.output);
    return;
  }
  if (result.needs_install) {
    setStatus('error', 'Chromium not installed');
    if (confirm('Chromium is required to render PDFs (~150 MB, one-time download).\n\nInstall it now?')) {
      runBrowserInstall();
    }
    return;
  }
  setStatus('error', 'Conversion failed');
  showToast('Error: ' + (result.error || 'Unknown error'), 'error');
}

function runBrowserInstall() {
  setStatus('working', 'Downloading Chromium (~150 MB)...');
  showToast('Downloading Chromium — this may take a minute', 'success');
  pywebview.api.install_browser().then(function(res) {
    if (res.success) {
      setStatus('ready', 'Chromium installed. Click Convert to retry.');
      showToast('Chromium installed!', 'success');
    } else {
      setStatus('error', 'Install failed');
      showToast('Install failed: ' + (res.error || 'exit code ' + res.exit_code), 'error');
    }
  }).catch(handleError);
}

function handleError(err) {
  btnConvert.disabled = false;
  setStatus('error', String(err));
  showToast('Error: ' + String(err), 'error');
}

// ────────────────────────────────────
// OUTPUT DIRECTORY
// ────────────────────────────────────

document.getElementById('btn-output-dir').addEventListener('click', () => {
  pywebview.api.choose_directory().then(function(dir) {
    if (dir) document.getElementById('output-dir').value = dir;
  });
});

// ────────────────────────────────────
// STATUS
// ────────────────────────────────────

function setStatus(state, msg) {
  statusIndicator.className = 'indicator ' + state;
  statusText.textContent = msg;
}

// ────────────────────────────────────
// TOAST
// ────────────────────────────────────

let toastTimer;
function showToast(msg, type) {
  toast.textContent = msg;
  toast.className = 'toast ' + type + ' show';
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { toast.className = 'toast'; }, 3000);
}

// ────────────────────────────────────
// KEYBOARD SHORTCUTS
// ────────────────────────────────────

document.addEventListener('keydown', function(e) {
  if ((e.ctrlKey || e.metaKey) && e.key === 'o') {
    e.preventDefault();
    btnOpen.click();
  }
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    e.preventDefault();
    if (!btnConvert.disabled) btnConvert.click();
  }
});
</script>
</body>
</html>"""


class MdToPdfAPI:
    def __init__(self) -> None:
        self._window: Any = None
        self._dropped_dir: Path | None = None

    def set_window(self, window: Any) -> None:
        self._window = window

    def load_settings(self) -> dict[str, Any]:
        return load_settings()

    def save_settings(self, settings_json: str) -> None:
        try:
            settings = json.loads(settings_json)
        except json.JSONDecodeError:
            return
        save_settings(settings)

    def load_file_from_content(self, name: str, content: str) -> dict[str, Any]:
        if self._dropped_dir is None:
            import tempfile
            self._dropped_dir = Path(tempfile.mkdtemp(prefix="md-to-pdf-drop-"))
        target = self._dropped_dir / name
        target.write_text(content, encoding="utf-8")
        return self.load_file(str(target))

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        if size_bytes < 1024:
            return f"{size_bytes} B"
        if size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        return f"{size_bytes / (1024 * 1024):.2f} MB"

    def load_file(self, file_path: str) -> dict[str, Any]:
        path = Path(file_path)
        if not path.is_file():
            return {"error": f"File not found: {file_path}"}

        content = path.read_text(encoding="utf-8")
        lines = content.count("\n") + 1
        preview_html = convert_to_html(path, css=load_default_css())

        return {
            "path": str(path),
            "name": path.name,
            "size": self._format_size(path.stat().st_size),
            "lines": lines,
            "preview_html": preview_html,
        }

    def choose_file(self) -> str | None:
        result = self._window.create_file_dialog(
            webview.OPEN_DIALOG,
            allow_multiple=False,
            file_types=("Markdown files (*.md;*.markdown)", "All files (*.*)"),
        )
        if not result:
            return None
        return result[0] if isinstance(result, (list, tuple)) else str(result)

    def choose_directory(self) -> str | None:
        dirs = self._window.create_file_dialog(
            webview.FOLDER_DIALOG,
            directory=str(Path.home()),
        )
        return dirs[0] if dirs else None

    def convert(self, file_path: str, settings_json: str) -> dict[str, Any]:
        try:
            settings: dict[str, Any] = json.loads(settings_json)
        except json.JSONDecodeError:
            settings = {}

        md_path = Path(file_path)
        if not md_path.is_file():
            return {"success": False, "error": f"File not found: {file_path}"}

        output_dir = (
            Path(settings["output_dir"])
            if settings.get("output_dir")
            else md_path.parent
        )
        output_path = output_dir / f"{md_path.stem}.pdf"
        page_size = settings.get("page_size", "A4")
        custom_css = settings.get("custom_css", "")

        base_css = load_default_css()
        full_css = base_css + "\n" + custom_css if custom_css.strip() else base_css

        try:
            output = md_to_pdf(
                md_path,
                output_path,
                css_content=full_css,
                title=md_path.stem,
                page_size=page_size,
            )
        except ChromiumNotInstalledError as exc:
            logger.warning("Chromium missing; user must run install_browser")
            return {
                "success": False,
                "needs_install": True,
                "error": str(exc),
            }
        except Exception as exc:
            logger.exception("PDF conversion failed")
            return {"success": False, "error": str(exc)}

        return {"success": True, "output": str(output)}

    def install_browser(self) -> dict[str, Any]:
        try:
            code = install_browser()
        except Exception as exc:
            logger.exception("Browser install crashed")
            return {"success": False, "error": str(exc)}
        return {"success": code == 0, "exit_code": code}

    def open_output(self, file_path: str) -> None:
        path = Path(file_path)
        if not path.exists():
            return
        if sys.platform == "win32":
            os.startfile(str(path))  # type: ignore[attr-defined]
        elif sys.platform == "darwin":
            subprocess.run(["open", str(path)], check=False)
        else:
            subprocess.run(["xdg-open", str(path)], check=False)


def run_gui() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    api = MdToPdfAPI()
    window = webview.create_window(
        title="MD → PDF Converter",
        html=GUI_HTML,
        js_api=api,
        width=1100,
        height=750,
        min_size=(900, 600),
    )
    api.set_window(window)
    webview.start(debug=False)