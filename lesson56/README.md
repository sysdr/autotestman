# Lesson 56: Handling Permissions

## Quick Start

This repo supports **two modes**:

- **Offline/unit mode (default)**: runs without Appium/emulator/APK. Useful to validate the permission-handler logic quickly.
- **Real device/emulator mode**: runs against an emulator/device via Appium and installs/launches your APK.

### Offline/unit mode (default)

```bash
python verify_result.py
pytest -q
```

### Real emulator/device mode (Windows)

1) Start emulator (example AVD `Pixel_7a`)

**CMD.exe**

```bat
"%LOCALAPPDATA%\Android\Sdk\emulator\emulator.exe" -avd Pixel_7a
"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe" wait-for-device
"%LOCALAPPDATA%\Android\Sdk\platform-tools\adb.exe" devices
```

2) Start Appium with Android SDK env vars set (same terminal)

**CMD.exe**

```bat
set ANDROID_SDK_ROOT=%LOCALAPPDATA%\Android\Sdk
set ANDROID_HOME=%LOCALAPPDATA%\Android\Sdk
appium --address 127.0.0.1 --port 4723
```

3) Run tests with a real APK (separate terminal)

**CMD.exe**

```bat
cd /d "C:\Users\syste\git\auto-testing\lesson56"
set USE_REAL_DEVICE=1
pytest .\tests\test_permission_handling.py -v --app-path "C:\FULL\PATH\TO\app-debug.apk" --app-package "com.your.package" --app-activity ".YourMainActivity"
```

## Key Concepts

| Layer | Mechanism | When It Acts |
|-------|-----------|--------------|
| Layer 1 | `autoGrantPermissions=True` | At APK install (session start) |
| Layer 2 | `PermissionHandler.handle()` | Mid-session popup appears |

## Passing Test Output

The tests are designed to pass in either of these situations:

- Permission popup never appears (because Layer 1 pre-granted it)
- Permission popup appears and Layer 2 finds and accepts it

## Notes

- `tests/conftest.py` exposes `--app-path`, `--app-package`, and `--app-activity` so you can point to any APK.
- For real device/emulator mode, you must have an Appium server running at `http://127.0.0.1:4723` and a connected device/emulator.
