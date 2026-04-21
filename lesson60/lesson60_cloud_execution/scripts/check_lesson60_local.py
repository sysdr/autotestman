#!/usr/bin/env python3
"""
scripts/check_lesson60_local.py — Pixel 7a / local Appium pre-flight.

Run from lesson60_cloud_execution (after copying .env.example → .env):
  python scripts/check_lesson60_local.py

Uses LOCAL_UDID (default emulator-5554), LOCAL_APPIUM_URL, LOCAL_APK_PATH from the environment.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_ROOT / ".env")


def main() -> int:
    udid = (os.environ.get("LOCAL_UDID") or "emulator-5554").strip()
    base = (os.environ.get("LOCAL_APPIUM_URL") or "http://127.0.0.1:4723").rstrip("/")

    adb = shutil.which("adb")
    if not adb:
        print(
            "FAIL: adb not in PATH. Add Android SDK platform-tools to PATH "
            "(e.g. ...\\Android\\Sdk\\platform-tools)."
        )
        return 1

    try:
        proc = subprocess.run(
            [adb, "devices"],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"FAIL: adb devices: {exc}")
        return 1

    lines = [
        ln.strip()
        for ln in proc.stdout.splitlines()
        if ln.strip() and not ln.startswith("List of devices")
    ]
    tab = chr(9)
    online: list[str] = []
    for ln in lines:
        if tab not in ln:
            continue
        did, st = ln.split(tab, 1)
        if st.strip() == "device":
            online.append(did.strip())

    if not online:
        print(
            "FAIL: No device in `adb devices` state=device. "
            "Start a Pixel 7a AVD in Android Studio and wait until fully booted."
        )
        return 2

    if udid not in online:
        print(
            f"FAIL: LOCAL_UDID={udid!r} is not online. "
            f"Active device(s): {online}. Set LOCAL_UDID in .env to match."
        )
        return 3

    try:
        with urlopen(f"{base}/status", timeout=5) as resp:  # noqa: S310
            resp.read(300)
    except (URLError, OSError) as exc:
        print(
            f"FAIL: Appium not reachable at {base}/status ({exc}). "
            "Start Appium 2 (e.g. `appium`) with UiAutomator2 driver installed."
        )
        return 4

    apk = (os.environ.get("LOCAL_APK_PATH") or "").strip()
    if not apk or apk == "/path/to/local.apk":
        print(
            "WARN: LOCAL_APK_PATH not set. Install the lesson Android sample .apk "
            "and set LOCAL_APK_PATH in .env (see .env.example)."
        )
        return 0

    if not Path(apk).is_file():
        print(f"FAIL: LOCAL_APK_PATH is not a file: {apk!r}")
        return 5

    print(
        "OK: adb + emulator + Appium + APK look ready. "
        "Run: set APPIUM_MODE=local (in .env) then pytest tests/test_cloud_login.py -v"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
