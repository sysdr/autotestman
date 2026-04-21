"""
conftest.py — UQAP Lesson 60
Pytest fixtures for cloud + local Appium execution.
Strategy pattern: swap driver backend without changing tests.
"""
from __future__ import annotations
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

import pytest
from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parent
load_dotenv(_ROOT / ".env")   # stable path even if pytest cwd differs
load_dotenv()                  # optional overrides from process cwd

# ── Inline import guard (gives a clear message if appium not installed) ──
try:
    from appium import webdriver
    from appium.options.android import UiAutomator2Options
    from appium.webdriver.common.appiumby import AppiumBy
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    APPIUM_AVAILABLE = True
except ImportError:
    APPIUM_AVAILABLE = False

def _resolve_appium_mode() -> str:
    """dry = stub driver (no account). cloud = real BrowserStack (needs BS_*). local = Appium+APK."""
    raw = (os.getenv("APPIUM_MODE") or "dry").strip().lower()
    if not raw:
        raw = "dry"
    if raw == "cloud":
        u = os.getenv("BS_USERNAME", "").strip()
        k = os.getenv("BS_ACCESS_KEY", "").strip()
        if not u or not k or u.startswith("your_") or k.startswith("your_"):
            print(
                "[lesson60] BS_USERNAME/BS_ACCESS_KEY missing or still placeholder → "
                "APPIUM_MODE=dry (stub driver). Set real creds for cloud runs."
            )
            return "dry"
        return "cloud"
    if raw == "local":
        return "local"
    if raw == "dry":
        return "dry"
    print(f"[lesson60] Unknown APPIUM_MODE={raw!r} → dry")
    return "dry"


APPIUM_MODE = _resolve_appium_mode()

# Logreport runs after the built-in makereport (firstresult); we only key by nodeid here.
_PENDING_APPIUM_SESSION: dict[str, str] = {}

# BrowserStack hub — swapped for SauceLabs by changing one env var
BS_HUB = "https://hub-cloud.browserstack.com/wd/hub"
SAUCE_HUB = "https://ondemand.us-west-1.saucelabs.com:443/wd/hub"
HUB_URL = os.getenv("APPIUM_HUB_URL", BS_HUB)


def _build_cloud_options() -> "UiAutomator2Options":
    """Build BrowserStack-compatible capability set from environment."""
    username = os.environ["BS_USERNAME"]
    access_key = os.environ["BS_ACCESS_KEY"]

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = os.getenv("BS_DEVICE", "Samsung Galaxy S21")
    options.platform_version = os.getenv("BS_OS_VERSION", "11.0")

    # Use the BrowserStack sample app (no APK upload needed for trial)
    options.app = os.getenv(
        "BS_APP_URL",
        "bs://c700ce60cf13ae8ed97705a55b8e022f13c5827e"   # BS demo app
    )

    # BrowserStack-specific options
    options.set_capability("bstack:options", {
        "userName": username,
        "accessKey": access_key,
        "buildName": os.getenv("BS_BUILD", "UQAP_CI"),
        "sessionName": "test_cloud_login",
        "projectName": "UQAP Mobile Suite",
        "debug": True,
        "networkLogs": True,
        "video": True,
    })
    return options


def _build_local_options() -> "UiAutomator2Options":
    """Capabilities for Appium + Android emulator (Pixel 7a AVD in Android Studio)."""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    # Friendly label; Appium targets the device via udid (must match `adb devices`).
    options.device_name = os.getenv("LOCAL_DEVICE_NAME", "Pixel 7a")
    udid = (os.getenv("LOCAL_UDID") or "emulator-5554").strip()
    if udid:
        options.udid = udid
    options.app = os.getenv("LOCAL_APK_PATH", "/path/to/local.apk")
    options.no_reset = False
    return options


class _DryRunElement:
    """Minimal element API for Lesson 60 dry-run (no cloud session)."""

    def is_displayed(self) -> bool:
        return True

    def is_enabled(self) -> bool:
        return True

    def click(self) -> None:
        return None

    def send_keys(self, *_args, **_kwargs) -> None:
        return None


class _DryRunDriver:
    """Stub WebDriver so tests pass without BrowserStack (educational smoke only)."""

    def __init__(self) -> None:
        self.session_id = "dry-run-lesson60"
        self._capabilities = {
            "platformName": "Android",
            "udid": "dry-run-no-farm-0001",
        }

    @property
    def capabilities(self) -> dict:
        return self._capabilities

    def implicitly_wait(self, _seconds: int) -> None:
        return None

    def find_element(self, _by, _value):  # noqa: ANN001
        return _DryRunElement()

    def quit(self) -> None:
        return None


@contextmanager
def _appium_driver() -> Generator:
    """
    Context manager: always calls driver.quit() even on crash.
    This is the core pattern that prevents session leaks.
    """
    if not APPIUM_AVAILABLE:
        raise RuntimeError(
            "appium-python-client not installed.\n"
            "Run: pip install appium-python-client"
        )

    if APPIUM_MODE == "dry":
        drv = _DryRunDriver()
        try:
            print("  APPIUM_MODE=dry — stub driver (no BrowserStack session).")
            yield drv
        finally:
            drv.quit()
        return

    if APPIUM_MODE == "local":
        apk = os.getenv("LOCAL_APK_PATH", "").strip()
        if not apk or apk == "/path/to/local.apk" or not Path(apk).is_file():
            pytest.skip(
                "Local mode: set LOCAL_APK_PATH to an existing APK and start Appium + emulator."
            )

    options = _build_cloud_options() if APPIUM_MODE == "cloud" else _build_local_options()
    hub = HUB_URL if APPIUM_MODE == "cloud" else os.getenv("LOCAL_APPIUM_URL", "http://localhost:4723")

    driver = None
    try:
        if APPIUM_MODE == "local":
            ap = Path(str(getattr(options, "app", "") or ""))
            print(
                f"  Local Appium → udid={getattr(options, 'udid', '')!r} "
                f"app={ap.name!r} hub={hub!r}"
            )
        print(
            f"  Connecting to {'cloud farm' if APPIUM_MODE == 'cloud' else 'local Appium'}..."
        )
        driver = webdriver.Remote(hub, options=options)
        driver.implicitly_wait(0)   # We use explicit waits only — no implicit
        yield driver
    finally:
        if driver:
            sid = driver.session_id
            driver.quit()           # ← THE CRITICAL LINE. Always executes.
            print(f"  Session closed: {sid}")


@pytest.fixture(scope="function")
def mobile_driver(request):
    """
    Pytest fixture wrapping the context manager.
    scope="function" means a fresh session per test (safest for cloud billing).
    """
    with _appium_driver() as drv:
        sid = drv.session_id
        setattr(request.node, "_appium_session_id", sid)
        _PENDING_APPIUM_SESSION[request.node.nodeid] = sid
        yield drv


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    """Write HTML/JSON after each test call (runs after built-in makereport)."""
    if report.when != "call":
        return
    sid = _PENDING_APPIUM_SESSION.pop(report.nodeid, None)
    if not sid:
        return
    try:
        from utils.reporter import save_session_report

        if report.outcome == "passed":
            status = "PASSED"
        elif report.outcome == "skipped":
            status = "SKIPPED"
        else:
            status = "FAILED"
        save_session_report(sid, report.nodeid, status, float(report.duration))
    except Exception as exc:  # noqa: BLE001 — never fail the run on reporting
        print(f"  [reporter] skipped: {exc}")
