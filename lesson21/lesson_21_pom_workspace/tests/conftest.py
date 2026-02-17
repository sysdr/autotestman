"""
Pytest configuration and fixtures.
Provides shared test fixtures for WebDriver and page objects.
Ensures test isolation: each test gets a clean browser state.
Uses Chrome only (ChromeDriver + Chrome browser), no third-party browsers.
"""

import os
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from utils.driver_manager import create_chrome_driver


def _use_visible_chrome() -> bool:
    """Use visible Chrome window when RUN_VISIBLE_CHROME=1 (default: headless)."""
    return os.environ.get("RUN_VISIBLE_CHROME", "").strip() in ("1", "true", "yes")


@pytest.fixture(scope="function")
def driver() -> WebDriver:
    """
    Provide a fresh Chrome WebDriver instance per test with clean state.
    Uses Chrome browser only (ChromeDriver). Set RUN_VISIBLE_CHROME=1 to see the browser.
    
    Yields:
        WebDriver instance
    """
    headless = not _use_visible_chrome()
    driver_instance = create_chrome_driver(headless=headless)
    try:
        # Clean state: no cookies or storage from previous runs
        driver_instance.delete_all_cookies()
        yield driver_instance
    finally:
        driver_instance.quit()


@pytest.fixture(scope="function")
def driver_visible() -> WebDriver:
    """
    Fixture for visible browser (useful for debugging).
    Same isolation guarantees as driver fixture.
    
    Yields:
        WebDriver instance with visible browser
    """
    driver_instance = create_chrome_driver(headless=False)
    try:
        driver_instance.delete_all_cookies()
        yield driver_instance
    finally:
        driver_instance.quit()
