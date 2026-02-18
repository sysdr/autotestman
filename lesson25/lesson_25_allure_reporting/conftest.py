"""Pytest configuration with Allure integration"""
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import SessionNotCreatedException
from pathlib import Path
import allure
from datetime import datetime


# Directory where Chrome and ChromeDriver should be present for tests (project-local)
_CONFTEST_DIR = Path(__file__).resolve().parent
CHROME_DIR = _CONFTEST_DIR / "chrome"   # Chrome binary: CHROME_DIR / "chrome"
DRIVER_DIR = _CONFTEST_DIR / "drivers"  # ChromeDriver: DRIVER_DIR / "chromedriver"
CHROMEDRIVER_PATH = DRIVER_DIR / "chromedriver"

# System Chrome paths (no third-party driver); first existing path is used.
# Project chrome/ first so tests find Chrome when run from any environment.
CHROME_PATHS = [
    str(CHROME_DIR / "chrome"),         # project-local (copy Chrome here if needed)
    "/opt/google/chrome/chrome",
    "/opt/google/chrome/google-chrome",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium-browser",
    "/usr/bin/chromium",
]


def _get_chrome_binary():
    """Use system Chrome: first path that exists and is executable."""
    for p in CHROME_PATHS:
        if os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    return None


@pytest.fixture(scope="function")
def driver(request):
    """Setup Chrome driver with screenshot on failure. Uses system Chrome + Selenium Manager for driver."""
    chrome_binary = _get_chrome_binary()
    if not chrome_binary:
        pytest.skip(
            "Chrome not found. Install Chrome and ensure it is at one of: "
            + ", ".join(CHROME_PATHS)
        )
    chrome_options = Options()
    chrome_options.binary_location = chrome_binary
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    # Use project ChromeDriver 144 so system /usr/bin/chromedriver (v145) is never used
    if not CHROMEDRIVER_PATH.is_file() or not os.access(CHROMEDRIVER_PATH, os.X_OK):
        pytest.skip(
            f"ChromeDriver not found at {CHROMEDRIVER_PATH}. "
            "Download ChromeDriver 144 for linux64 and place as drivers/chromedriver."
        )
    service = Service(executable_path=str(CHROMEDRIVER_PATH))
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except SessionNotCreatedException as e:
        if "no chrome binary" in str(e).lower():
            pytest.skip(
                "Chrome binary not accessible to ChromeDriver (e.g. sandbox). "
                "Run pytest from your system terminal where Chrome is installed."
            )
        raise
    driver.implicitly_wait(5)
    
    yield driver
    
    # Screenshot on failure
    if request.node.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_name = f"{request.node.name}_{timestamp}"
        
        # Save to file
        screenshot_path = Path("screenshots") / f"{screenshot_name}.png"
        driver.save_screenshot(str(screenshot_path))
        
        # Attach to Allure
        allure.attach(
            driver.get_screenshot_as_png(),
            name=screenshot_name,
            attachment_type=allure.attachment_type.PNG
        )
        
        # Attach page source
        allure.attach(
            driver.page_source,
            name="page_source",
            attachment_type=allure.attachment_type.HTML
        )
        
        # Attach browser logs
        try:
            logs = driver.get_log('browser')
            allure.attach(
                str(logs),
                name="browser_logs",
                attachment_type=allure.attachment_type.TEXT
            )
        except:
            pass
    
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test outcome for screenshot logic"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="session", autouse=True)
def allure_environment_info():
    """Add environment info to Allure report"""
    env_path = Path("allure-results") / "environment.properties"
    env_path.parent.mkdir(exist_ok=True)
    
    environment_info = {
        "Browser": "Chrome Headless",
        "Python.Version": "3.11+",
        "Framework": "Pytest + Selenium",
        "Test.Environment": "Local"
    }
    
    with open(env_path, "w") as f:
        for key, value in environment_info.items():
            f.write(f"{key}={value}\n")
