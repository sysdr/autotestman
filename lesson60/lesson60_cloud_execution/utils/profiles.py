"""
utils/profiles.py — UQAP Lesson 60
Load named capability profiles from config/capability_profiles.json.
"""
from __future__ import annotations
import json
from pathlib import Path

_CONFIG = Path(__file__).resolve().parent.parent / "config" / "capability_profiles.json"


def load_capability_profiles() -> dict:
    return json.loads(_CONFIG.read_text(encoding="utf-8"))


def get_profile(name: str) -> dict:
    data = load_capability_profiles()
    profiles = data.get("profiles", {})
    if name not in profiles:
        raise KeyError(f"Unknown capability profile: {name!r}")
    return profiles[name]
