"""
Pytest configuration and fixtures for window handling tests.
"""

import os
import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# Project root (lesson18_window_handling); resolve so symlinks are real paths
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_PROJECT_BIN = _PROJECT_ROOT / "bin"
_PROJECT_DRIVER = _PROJECT_ROOT / "driver" / "chromedriver"
_BROWSER_NAMES_IN_BIN = ("chromium", "google-chrome", "chromium-browser")
_SYSTEM_BROWSER_PATHS = [
    Path("/usr/bin/google-chrome"),
    Path("/usr/bin/chromium"),
    Path("/usr/bin/chromium-browser"),
]


def _resolve_chrome_binary(path):
    """Return path to actual Chrome binary; use same-dir 'chrome' when path is a wrapper script."""
    resolved = Path(path).resolve()
    # Google Chrome install often has wrapper script 'google-chrome' and real binary 'chrome'
    same_dir_chrome = resolved.parent / "chrome"
    if same_dir_chrome.exists():
        return str(same_dir_chrome.resolve())
    return str(resolved)


def _find_chrome_binary():
    """Look in project bin/ first, then system paths. Return resolved path or None."""
    for name in _BROWSER_NAMES_IN_BIN:
        p = _PROJECT_BIN / name
        if p.exists():
            return _resolve_chrome_binary(p)
    for p in _SYSTEM_BROWSER_PATHS:
        if p.exists():
            return _resolve_chrome_binary(p)
    return None


def _find_chromedriver():
    """Look for project-local driver. Return resolved path or None (then use Selenium Manager)."""
    if _PROJECT_DRIVER.exists():
        return str(_PROJECT_DRIVER.resolve())
    return None


@pytest.fixture(scope="function")
def driver():
    """
    Provide a fresh Chrome WebDriver instance for each test.

    Browser: project bin/ (chromium, google-chrome, chromium-browser) then system paths.
    Driver: project driver/chromedriver if present, else Selenium Manager / PATH.
    No third-party driver downloads; paths are resolved to avoid symlink issues.
    """
    options = Options()

    # Run headless unless explicitly disabled
    if os.getenv("HEADED") != "1":
        options.add_argument("--headless=new")

    # Use project or system Chrome/Chromium binary (resolved to real binary, not wrapper script)
    chrome_binary = _find_chrome_binary()
    if chrome_binary:
        options.binary_location = chrome_binary

    # Essential for Docker/CI environments
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    # Set consistent window size
    options.add_argument("--window-size=1920,1080")

    # Reduce noise in logs
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Driver: project driver/chromedriver if present (resolved), else Selenium Manager.
    # When using Selenium Manager, hide system chromedriver from PATH so a version-matching
    # driver is used (system /usr/bin chromedriver may not match installed Chrome).
    chromedriver_path = _find_chromedriver()
    if chromedriver_path:
        service = Service(chromedriver_path)
        driver_instance = webdriver.Chrome(service=service, options=options)
    else:
        saved_path = os.environ.get("PATH", "")
        try:
            restricted = ":".join(
                p for p in saved_path.split(":") if p not in ("/usr/bin", "/bin")
            )
            if restricted != saved_path:
                os.environ["PATH"] = restricted
            driver_instance = webdriver.Chrome(options=options)
        finally:
            os.environ["PATH"] = saved_path

    # Set implicit wait (backup for explicit waits)
    driver_instance.implicitly_wait(2)

    yield driver_instance

    # Cleanup
    driver_instance.quit()


@pytest.fixture(scope="session")
def demo_page_url():
    """
    Provide URL to demo HTML page.
    
    Creates a simple HTTP server for the demo page if needed.
    """
    # For this lesson, we'll use a file:// URL to the demo page
    demo_file = Path(__file__).parent.parent / "demo_page.html"
    
    if not demo_file.exists():
        raise FileNotFoundError(f"Demo page not found at {demo_file}")
    
    return demo_file.as_uri()


@pytest.fixture(autouse=True)
def verify_window_count(driver):
    """
    Automatic fixture that verifies no window leaks after each test.
    
    Production safety check: ensures tests clean up properly.
    """
    initial_count = len(driver.window_handles)
    
    yield
    
    final_count = len(driver.window_handles)
    
    if final_count != initial_count:
        # Force cleanup of leaked windows
        main_handle = driver.window_handles[0]
        for handle in driver.window_handles[1:]:
            driver.switch_to.window(handle)
            driver.close()
        driver.switch_to.window(main_handle)
        
        pytest.fail(
            f"WINDOW LEAK DETECTED: Started with {initial_count} windows, "
            f"ended with {final_count}. Leaked windows were force-closed."
        )
