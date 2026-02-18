"""
Demo tests to showcase automatic screenshot capture.
These tests intentionally include failures to trigger our screenshot mechanism.
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_google_homepage_loads(driver_init):
    """
    A passing test - no screenshot should be generated.
    This proves our hook only triggers on actual failures.
    """
    driver = driver_init
    driver.get("https://www.google.com")
    
    # Wait for search box to be present
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    
    assert search_box is not None
    assert "Google" in driver.title


def test_google_search_functionality(driver_init):
    """
    Another passing test with actual interaction.
    """
    driver = driver_init
    driver.get("https://www.google.com")
    
    # Find search box and perform search
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.send_keys("Python SDET")
    search_box.submit()
    
    # Wait for results: URL contains search + query, or document title is set (id="search" not always present)
    WebDriverWait(driver, 15).until(
        lambda d: ("search" in d.current_url and "Python" in d.current_url)
                 or (not d.title.startswith("http") and "Python" in d.title)
    )
    
    assert "Python" in driver.title or ("search" in driver.current_url and "Python" in driver.current_url)


def test_intentional_failure_assertion(driver_init):
    """
    This test INTENTIONALLY fails to demonstrate screenshot capture.
    
    When this fails, our pytest hook will:
    1. Detect the failure in pytest_runtest_makereport
    2. Extract the driver from item.driver
    3. Generate a unique filename
    4. Save the screenshot to screenshots/YYYY-MM-DD/
    """
    driver = driver_init
    driver.get("https://www.google.com")
    
    # Wait for page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    
    # This assertion will fail - title is "Google", not "Yahoo"
    assert "Yahoo" in driver.title, "Expected Yahoo but got Google"


def test_intentional_failure_missing_element(driver_init):
    """
    Another intentional failure - element not found.
    This simulates a real-world scenario where the UI changed.
    """
    driver = driver_init
    driver.get("https://www.google.com")
    
    # Wait for a non-existent element (will timeout and fail)
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "non_existent_element_12345"))
        )
    except Exception:
        # Force an assertion failure to trigger screenshot
        assert False, "Expected element was not found on the page"


@pytest.mark.skip(reason="Example of a skipped test - no screenshot needed")
def test_skipped_example(driver_init):
    """
    Skipped tests don't trigger screenshots.
    This is expected behavior - we only want evidence of actual failures.
    """
    assert True
