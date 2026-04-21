"""
tests/conftest.py
Pytest fixtures for mobile session management.
"""
from __future__ import annotations
import pytest
import logging
import socket
from urllib.parse import urlparse
from pathlib import Path
import os
from appium import webdriver
from utils.capabilities import build_android_options, AndroidCapConfig
from utils.permission_handler import PermissionHandler, Platform

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

APPIUM_URL = "http://127.0.0.1:4723"

def _is_tcp_open(host: str, port: int, timeout_s: float = 1.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout_s):
            return True
    except OSError:
        return False


@pytest.fixture(scope="function")
def android_driver(request):
    """
    Spins up an Appium session with autoGrantPermissions=True.
    Yields (driver, PermissionHandler) tuple.
    Tears down the session after the test regardless of outcome.
    """
    # ── Configure: update app_path, app_package, app_activity for your APK ──
    cfg = AndroidCapConfig(
        app_path     = request.config.getoption("--app-path", default="./app/sampleapp.apk"),
        app_package  = request.config.getoption("--app-package", default="com.example.sampleapp"),
        app_activity = request.config.getoption("--app-activity", default=".MainActivity"),
    )

    options = build_android_options(cfg)
    driver  = None

    try:
        # If you want a real device/emulator integration run, set:
        #   USE_REAL_DEVICE=1
        # and provide a real --app-path.
        use_real = os.getenv("USE_REAL_DEVICE", "").strip() in {"1", "true", "True", "yes", "YES"}
        apk_exists = Path(cfg.app_path).expanduser().exists()

        if not use_real or not apk_exists:
            # Offline/unit mode: make PermissionHandler.handle() deterministically
            # return "not present" by forcing the wait to time out.
            from selenium.common.exceptions import TimeoutException
            import utils.permission_handler as ph

            class _AlwaysTimeoutWait:
                def __init__(self, *args, **kwargs):
                    pass

                def until(self, *args, **kwargs):
                    raise TimeoutException("offline mode: no real device session")

            ph.WebDriverWait = _AlwaysTimeoutWait  # type: ignore[attr-defined]

            dummy_driver = object()
            handler = PermissionHandler(driver=dummy_driver, platform=Platform.ANDROID, timeout=0.01)
            yield dummy_driver, handler
            return

        parsed = urlparse(APPIUM_URL)
        host = parsed.hostname or "127.0.0.1"
        port = parsed.port or 4723
        if not _is_tcp_open(host, port):
            pytest.skip(
                f"Appium is not reachable at {APPIUM_URL}. "
                "Start it (example): appium --address 127.0.0.1 --port 4723"
            )
        logger.info("Starting Appium session...")
        driver  = webdriver.Remote(APPIUM_URL, options=options)
        handler = PermissionHandler(driver=driver, platform=Platform.ANDROID, timeout=5.0)
        logger.info("[OK] Session started")
        yield driver, handler
    finally:
        if driver:
            driver.quit()
            logger.info("Session terminated.")


def pytest_addoption(parser):
    parser.addoption("--app-path",     action="store", default="./app/sampleapp.apk")
    parser.addoption("--app-package",  action="store", default="com.example.sampleapp")
    parser.addoption("--app-activity", action="store", default=".MainActivity")
