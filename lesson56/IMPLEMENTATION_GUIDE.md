# Implementation Guide — Lesson 56 (Handling Permissions)

## Overview

This project demonstrates a **two-layer permission strategy** for mobile automation:

- **Layer 1 (pre-grant)**: request the OS to grant permissions automatically at install/session start (best-effort).
- **Layer 2 (runtime handler)**: if a permission popup still appears, detect it with an explicit wait and accept it.

The codebase is written in Python and is designed to be used with **Appium + Android emulator/device**. It also supports an **offline/unit mode** (no emulator required) to validate the permission-handler logic quickly.

## Architecture

- **`utils/permission_handler.py`**
  - Provides `PermissionHandler` and a registry of platform-specific locators.
  - Uses explicit waits to detect permission dialogs and click “Allow”.
  - Treats “popup not present” as a valid outcome (e.g., permission pre-granted).
- **`utils/capabilities.py`**
  - Builds Appium options/capabilities.
  - Enables Android permission pre-grant via `autoGrantPermissions=True`.
- **`tests/conftest.py`**
  - Provides a pytest fixture that either:
    - runs **offline/unit mode** (default), or
    - creates a real Appium session when `USE_REAL_DEVICE=1` and a real APK is supplied.
- **`tests/test_permission_handling.py`**
  - Exercises the permission handling behaviors (single popup, multiple popups, idempotency).

## Project layout

Inside `lesson56/`:

- `utils/`
  - `permission_handler.py`
  - `capabilities.py`
- `tests/`
  - `conftest.py`
  - `test_permission_handling.py`
- `verify_result.py`: checks that required files exist and imports resolve
- `requirements.txt`: Python dependencies
- `README.md`: how to run in offline mode and real emulator/device mode
- `.gitignore`: ignores caches/venvs/secrets
- `cleanup.sh`: stops containers and removes local caches

## Design

### Permission popups are not deterministic

On real devices/emulators, permission popups may:

- never appear (already granted, OS version behavior, app state),
- appear once, or
- appear in a different layout depending on Android version / OEM skin.

The design goal is **test continuity**:

- If a popup is detected, accept it.
- If it’s not detected within the timeout, continue (log it as informational).

### Two-layer strategy

- Layer 1 reduces flakiness by attempting to avoid popups entirely.
- Layer 2 absorbs remaining real-world cases where popups still show up.

## API

Main classes and functions:

- `PermissionHandler(driver, platform, timeout)`
  - `handle(popup_type) -> PermissionResult`
  - `handle_all([popup_type, ...]) -> list[PermissionResult]`
- `build_android_options(AndroidCapConfig) -> UiAutomator2Options`

## Dashboard/metrics

This lesson project does **not** include a dashboard or metrics pipeline. If you want metrics (e.g., popup present/accepted counts, elapsed time), a straightforward extension is to:

- export `PermissionResult` fields to logs/JSON,
- ship them to your metrics stack (Prometheus, ELK, etc.),
- render them in a dashboard.

## Build and run

### Prerequisites (real device/emulator mode)

- Android SDK installed (default Windows path often: `%LOCALAPPDATA%\Android\Sdk`)
- An Android emulator or real device reachable by `adb`
- Appium server with the **UiAutomator2** driver installed
- A real APK file to test

### Install Python dependencies

From `lesson56/`:

```bash
pip install -r requirements.txt
```

### Verify project structure/imports

From `lesson56/`:

```bash
python verify_result.py
```

## Docker

This project does not require Docker to run tests. A `cleanup.sh` script is included to:

- stop running containers (if any),
- prune unused docker resources,
- remove local test caches.

Run from `lesson56/`:

```bash
bash cleanup.sh
```

## Tests

### Offline/unit mode (default)

From `lesson56/`:

```bash
pytest -q
```

This mode does **not** create an Appium session and does not need an emulator.

### Real emulator/device mode (Windows CMD example)

Start emulator:

```bat
"%LOCALAPPDATA%\Android\Sdk\emulator\emulator.exe" -avd Pixel_7a
"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe" wait-for-device
"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe" devices
```

Start Appium with SDK environment variables (same terminal):

```bat
set ANDROID_SDK_ROOT=%LOCALAPPDATA%\Android\Sdk
set ANDROID_HOME=%LOCALAPPDATA%\Android\Sdk
appium --address 127.0.0.1 --port 4723
```

Run tests with your APK (separate terminal):

```bat
cd /d "<PATH>\lesson56"
set USE_REAL_DEVICE=1
pytest .\tests\test_permission_handling.py -v --app-path "C:\FULL\PATH\TO\app-debug.apk" --app-package "com.your.package" --app-activity ".YourMainActivity"
```

## Summary

- Use **offline/unit mode** for fast validation of permission-handler logic.
- Use **real device/emulator mode** for true end-to-end verification with Appium.
- Keep permission handling resilient: missing popups should not fail tests by default.
