
"""
Pytest configuration and fixtures for frame testing.
Uses Selenium built-in driver only; no third-party chromedriver.
Looks for browser and driver in project paths first, then system paths.
"""
import shutil
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# Project root (lesson_17_frames)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _resolve_path(p: Path) -> str:
    """Return absolute real path (resolve symlinks) so ChromeDriver gets the actual binary."""
    try:
        return str(p.resolve())
    except (OSError, RuntimeError):
        return str(p.absolute())


def _get_chrome_binary():
    """
    Browser binary: project bin/ first, then system paths.
    Symlinks are resolved to the real path so ChromeDriver can find the binary.
    """
    project_bin = [
        _PROJECT_ROOT / "bin" / "chromium",
        _PROJECT_ROOT / "bin" / "google-chrome",
        _PROJECT_ROOT / "bin" / "chromium-browser",
    ]
    for p in project_bin:
        if p.exists():
            return _resolve_path(p)
    system_paths = [
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium",
        "/snap/bin/chromium",
    ]
    for path in system_paths:
        if Path(path).exists():
            return _resolve_path(Path(path))
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        path = shutil.which(name)
        if path:
            return _resolve_path(Path(path))
    return None


def _get_chromedriver_path():
    """
    ChromeDriver path: project driver/ first (genuine driver only; no download).
    Symlinks are resolved to the real path.
    """
    project_driver = _PROJECT_ROOT / "driver" / "chromedriver"
    if project_driver.exists():
        return _resolve_path(project_driver)
    return None


@pytest.fixture(scope="function")
def driver():
    """
    Create a Chrome WebDriver instance for each test.
    Uses project driver/ or Selenium Manager; project bin/ or system for browser.
    """
    options = Options()
    binary = _get_chrome_binary()
    if binary:
        options.binary_location = binary
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver_path = _get_chromedriver_path()
    if driver_path:
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(0)  # Disable implicit waits, use explicit only

    yield driver

    # Cleanup
    driver.quit()


@pytest.fixture(autouse=True)
def reset_frame_context(driver):
    """
    Automatically reset frame context after each test.
    Prevents context pollution between tests.
    """
    yield
    # This runs after each test
    driver.switch_to.default_content()


@pytest.fixture(scope="session")
def test_page_url():
    """Return file:// URL for local test page"""
    html_file = Path(__file__).parent.parent / "resources" / "test_frames.html"
    return f"file://{html_file.absolute()}"
