"""
UQAP conftest.py — Session-scoped driver with Docker-safe Chrome flags.
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def _in_docker() -> bool:
    return Path("/.dockerenv").exists()


def _resolve_chrome_binary() -> str | None:
    """Locate Chrome/Chromium (WSL/Linux); override with CHROME_BIN."""
    env = os.environ.get("CHROME_BIN", "").strip()
    if env and Path(env).is_file():
        return env
    for name in ("google-chrome-stable", "google-chrome", "chromium", "chromium-browser"):
        p = shutil.which(name)
        if p and Path(p).is_file():
            return p
    for fixed in (
        "/opt/google/chrome/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/snap/bin/chromium",
    ):
        if Path(fixed).is_file():
            return fixed
    return None


def _chromedriver_service() -> Service:
    """
    In Docker, Selenium Manager picks a driver for the image Chrome.
    Locally, avoid a mismatched /usr/bin/chromedriver (common on dev machines).
    """
    if _in_docker():
        return Service()
    path = ChromeDriverManager().install()
    p = Path(path)
    # webdriver-manager 4.x may return THIRD_PARTY_NOTICES.chromedriver from newer zips.
    if p.name != "chromedriver" and (p.parent / "chromedriver").is_file():
        path = str(p.parent / "chromedriver")
    return Service(path)


def _build_chrome_options() -> Options:
    """
    Construct Chrome options that work both locally and inside Docker.

    The three Docker-mandatory flags:
      --no-sandbox           : Chrome sandbox needs Linux capabilities Docker strips.
      --disable-dev-shm-usage: Docker limits /dev/shm to 64MB; Chrome uses it for IPC.
      --headless=new         : No display server in a container.
    """
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1920,1080")
    opts.add_argument("--disable-extensions")
    return opts


@pytest.fixture(scope="session")
def driver():
    """
    Session-scoped WebDriver. One browser for the entire test run.
    'yield' ensures quit() is called even on failure — no orphan Chrome processes.
    """
    options = _build_chrome_options()
    binary = _resolve_chrome_binary()
    if binary:
        options.binary_location = binary
    elif not _in_docker():
        pytest.skip(
            "Chrome/Chromium not found. Install Google Chrome, set CHROME_BIN, "
            "or run tests in Docker: ./run_tests.sh"
        )

    drv = webdriver.Chrome(service=_chromedriver_service(), options=options)
    drv.implicitly_wait(10)
    yield drv
    drv.quit()
