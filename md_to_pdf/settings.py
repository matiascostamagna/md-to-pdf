"""Persistent user settings for the GUI (output dir, page size, custom CSS)."""

from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

DEFAULTS: dict[str, Any] = {
    "output_dir": "",
    "page_size": "A4",
    "custom_css": "",
}


def _config_dir() -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", str(Path.home() / "AppData" / "Roaming")))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config")))
    return base / "md-to-pdf"


def config_path() -> Path:
    return _config_dir() / "settings.json"


def load_settings() -> dict[str, Any]:
    path = config_path()
    if not path.is_file():
        return dict(DEFAULTS)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning("Could not read settings (%s); using defaults", exc)
        return dict(DEFAULTS)
    merged = dict(DEFAULTS)
    merged.update({k: v for k, v in data.items() if k in DEFAULTS})
    return merged


def save_settings(settings: dict[str, Any]) -> None:
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    sanitized = {k: settings.get(k, DEFAULTS[k]) for k in DEFAULTS}
    path.write_text(json.dumps(sanitized, indent=2), encoding="utf-8")
