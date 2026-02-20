"""
Pytest Configuration
====================
Fixtures and hooks for cross-browser testing.
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.browser_factory import BrowserFactory, BrowserConfig
from config.test_config import config


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--browser",
        action="store",
        default=None,
        help="Run tests on Chrome (chrome only)"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browsers in headless mode"
    )
    parser.addoption(
        "--slow",
        type=float,
        default=0,
        help="Delay in seconds after each action (e.g. 1.5) so you can watch the test"
    )


@pytest.fixture(params=["chrome"])
def browser(request):
    """
    Fixture that creates a Chrome browser instance.
    Use --browser=chrome to run on Chrome (default).
    """
    # Check if specific browser requested via CLI
    browser_option = request.config.getoption("--browser")
    if browser_option and browser_option != request.param:
        pytest.skip(f"Skipping {request.param}, running only {browser_option}")
    
    headless = request.config.getoption("--headless")
    
    # Create driver
    print(f"\n🌐 Launching {request.param.upper()}...")
    driver = BrowserFactory.create_driver(
        request.param,
        headless=headless,
        options=config.get_browser_options(request.param)
    )
    
    # Configure driver
    BrowserConfig.configure_driver(driver)
    
    # Attach browser name and action delay for reporting / slow mode
    driver.browser_name = request.param
    driver.action_delay = request.config.getoption("--slow", default=0)
    
    yield driver
    
    # Teardown
    print(f"\n🔚 Closing {request.param.upper()}...")
    driver.quit()


@pytest.fixture
def base_url():
    """Return the base URL for tests."""
    return config.base_url


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for reporting."""
    outcome = yield
    rep = outcome.get_result()
    
    # Store result in item for access in fixtures
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(autouse=True)
def screenshot_on_failure(request, browser):
    """Take screenshot on test failure."""
    yield
    
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        if config.screenshot_on_failure:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"failure_{browser.browser_name}_{timestamp}.png"
            screenshot_path = Path("reports") / screenshot_name
            browser.save_screenshot(str(screenshot_path))
            print(f"\n📸 Screenshot saved: {screenshot_path}")
