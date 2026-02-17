"""
Test suite for alert handling patterns.

Tests demonstrate:
- Basic alert interaction (accept/dismiss)
- Confirm dialog handling
- Prompt dialog with user input
- Delayed alerts (testing explicit waits)
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.alert_handler import AlertHandler, AlertUtils
from pages.alert_page import AlertDemoPage

# Genuine browser+driver pairs (same package, matching versions)
_SNAP_CHROME = Path("/snap/chromium/current/usr/lib/chromium-browser/chrome")
_SNAP_CHROMEDRIVER = Path("/snap/chromium/current/usr/lib/chromium-browser/chromedriver")


def _get_chrome_driver():
    """Use genuine Chrome/Chromium + matching ChromeDriver when available; else Selenium Manager."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    if _SNAP_CHROME.exists() and _SNAP_CHROMEDRIVER.exists():
        chrome_options.binary_location = str(_SNAP_CHROME)
        service = Service(executable_path=str(_SNAP_CHROMEDRIVER))
        return webdriver.Chrome(service=service, options=chrome_options)
    return webdriver.Chrome(options=chrome_options)


@pytest.fixture
def driver():
    """Fixture to create and teardown WebDriver. Uses genuine ChromeDriver when available."""
    driver = _get_chrome_driver()
    yield driver
    driver.quit()


def test_js_alert_accept(driver):
    """
    Test accepting a basic JavaScript alert.

    Demonstrates:
    - Context manager usage
    - Reading alert text
    - Accepting alert
    - Verifying result
    """
    page = AlertDemoPage(driver)
    page.load()

    # Trigger alert
    page.click_js_alert()

    # Handle alert using context manager
    with AlertHandler(driver, timeout=10) as alert:
        alert_text = alert.text
        assert alert_text == "This is a JS Alert", f"Unexpected alert text: {alert_text}"
        alert.accept()

    # Verify result
    result = page.get_result_text()
    assert "You clicked OK" in result, f"Unexpected result: {result}"


def test_js_confirm_accept(driver):
    """Test accepting a confirm dialog."""
    page = AlertDemoPage(driver)
    page.load()

    page.click_js_confirm()

    with AlertHandler(driver) as alert:
        assert "JS Confirm" in alert.text
        alert.accept()

    result = page.get_result_text()
    assert "You clicked OK" in result


def test_js_confirm_dismiss(driver):
    """Test dismissing a confirm dialog."""
    page = AlertDemoPage(driver)
    page.load()

    page.click_js_confirm()

    with AlertHandler(driver) as alert:
        alert.dismiss()

    result = page.get_result_text()
    assert "You clicked Cancel" in result


def test_js_prompt_with_input(driver):
    """
    Test sending text to a prompt dialog.

    Demonstrates:
    - Sending keys to alert
    - Custom user input handling
    """
    page = AlertDemoPage(driver)
    page.load()

    page.click_js_prompt()

    test_name = "Production SDET"
    with AlertHandler(driver) as alert:
        alert.send_keys(test_name)
        alert.accept()

    result = page.get_result_text()
    assert test_name in result, f"Expected '{test_name}' in result, got: {result}"


def test_delayed_alert(driver):
    """
    Test handling delayed alert (500ms).

    This is critical - demonstrates that explicit waits
    handle variable timing without time.sleep().
    """
    page = AlertDemoPage(driver)
    page.load()

    page.click_delayed_alert()

    # No time.sleep() needed! Explicit wait handles the delay
    with AlertHandler(driver, timeout=10) as alert:
        assert "500ms delay" in alert.text
        alert.accept()

    result = page.get_result_text()
    assert "Delayed alert was handled" in result


def test_alert_utils_accept(driver):
    """Test convenience utility for accepting alerts."""
    page = AlertDemoPage(driver)
    page.load()

    page.click_js_alert()

    # Using utility method
    alert_text = AlertUtils.accept_alert(driver, timeout=10)

    assert alert_text == "This is a JS Alert"
    assert "You clicked OK" in page.get_result_text()


def test_alert_utils_dismiss(driver):
    """Test convenience utility for dismissing alerts."""
    page = AlertDemoPage(driver)
    page.load()

    page.click_js_confirm()

    alert_text = AlertUtils.dismiss_alert(driver, timeout=10)

    assert "JS Confirm" in alert_text
    assert "You clicked Cancel" in page.get_result_text()


def test_alert_utils_send_keys(driver):
    """Test convenience utility for prompt input."""
    page = AlertDemoPage(driver)
    page.load()

    page.click_js_prompt()

    AlertUtils.send_keys_to_prompt(driver, "Automated Test", timeout=10)

    assert "Automated Test" in page.get_result_text()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])