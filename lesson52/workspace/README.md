# Lesson 52 Workspace — Appium Inspector (Inspector-as-Code)

Programmatic Appium UI inspection: parse UI hierarchy (XML), extract locators, and generate a locators file and HTML report. Works with a live Appium session or a local XML fixture (demo mode).

## Prerequisites

- Python 3.10+ recommended
- **Demo mode:** no Appium or device required
- **Live mode:** Android emulator or device, Appium 2.x with UiAutomator2, and an APK matching `config/appium_caps.py`

## Install

From this directory (`workspace/`):

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\activate`.

## Quick start

1. **Demo mode** (no device/Appium):

   ```bash
   DEMO_MODE=true pytest tests/ -v
   ```

   Uses `fixtures/login_screen.xml`; all tests should pass.

2. **Live Appium** (device/emulator + Appium on port 4723):

   - Put your APK in `apks/app-debug.apk` and set `APP_PACKAGE` / `APP_ACTIVITY` in `config/appium_caps.py`.
   - Run: `DEMO_MODE=false pytest tests/ -v`

## Layout

- `config/appium_caps.py` — Appium capabilities and host.
- `fixtures/login_screen.xml` — Sample UI hierarchy for demo.
- `locators/` — Generated locators (e.g. `login_screen_locators.py`).
- `pages/login_page.py` — Page Object using generated locators.
- `reports/` — Generated HTML inspection report.
- `utils/inspector.py` — AppiumInspector, OfflineInspector, write_locators.
- `utils/report_generator.py` — HTML report generation.
- `tests/test_appium_inspector.py` — Pytest suite.
- `cleanup.sh` — Stops Docker containers, prunes unused Docker resources, optionally stops the Docker systemd unit.
- `requirements.txt` — Python dependencies for tests and live Appium.

## Docker

This lesson does not run the app or tests inside Docker by default. To free disk space and stop leftover containers, from this directory run:

```bash
./cleanup.sh
```

If your Docker daemon is managed by systemd, the script attempts to stop the `docker` service after pruning (may require `sudo`).

## Security

There are no API keys in this workspace. Do not commit real credentials, keystores, or production APKs; keep secrets out of `config/` and use local env files that stay gitignored.
