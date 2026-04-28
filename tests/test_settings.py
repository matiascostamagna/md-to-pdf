"""Tests for persistent GUI settings."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from md_to_pdf import settings as settings_mod


@pytest.fixture
def tmp_config(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    cfg = tmp_path / "settings.json"
    monkeypatch.setattr(settings_mod, "config_path", lambda: cfg)
    return cfg


def test_load_settings_returns_defaults_when_no_file(tmp_config: Path) -> None:
    assert not tmp_config.exists()
    loaded = settings_mod.load_settings()
    assert loaded == settings_mod.DEFAULTS


def test_load_settings_returns_defaults_on_invalid_json(tmp_config: Path) -> None:
    tmp_config.parent.mkdir(parents=True, exist_ok=True)
    tmp_config.write_text("{not valid json", encoding="utf-8")
    assert settings_mod.load_settings() == settings_mod.DEFAULTS


def test_save_then_load_roundtrip(tmp_config: Path) -> None:
    settings_mod.save_settings({
        "output_dir": "/tmp/out",
        "page_size": "Letter",
        "custom_css": "body{color:red}",
    })

    assert tmp_config.is_file()
    loaded = settings_mod.load_settings()
    assert loaded["output_dir"] == "/tmp/out"
    assert loaded["page_size"] == "Letter"
    assert loaded["custom_css"] == "body{color:red}"


def test_save_strips_unknown_keys(tmp_config: Path) -> None:
    settings_mod.save_settings({"page_size": "A3", "evil_key": "bad"})
    raw = json.loads(tmp_config.read_text(encoding="utf-8"))
    assert "evil_key" not in raw
    assert raw["page_size"] == "A3"


def test_load_merges_partial_with_defaults(tmp_config: Path) -> None:
    tmp_config.parent.mkdir(parents=True, exist_ok=True)
    tmp_config.write_text(json.dumps({"page_size": "Legal"}), encoding="utf-8")

    loaded = settings_mod.load_settings()
    assert loaded["page_size"] == "Legal"
    assert loaded["output_dir"] == settings_mod.DEFAULTS["output_dir"]
    assert loaded["custom_css"] == settings_mod.DEFAULTS["custom_css"]
