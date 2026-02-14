
'''Tests for dropdown handling functionality.'''

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from pages.dropdown_page import DropdownTestPage
from pathlib import Path
import time
import os


@pytest.fixture
def driver():
    '''Setup Chrome driver with appropriate options.'''
    service = Service(os.path.join(os.getcwd(), "chromedriver"))
    driver = webdriver.Chrome(service=service)

    yield driver

    driver.quit()


@pytest.fixture
def dropdown_page(driver):
    '''Navigate to test page and return page object.'''
    test_page_path = Path(__file__).parent.parent / "fixtures" / "test_page.html"
    driver.get(f"file://{test_page_path.absolute()}")
    return DropdownTestPage(driver)


def test_native_dropdown_selection(dropdown_page):
    '''Test selecting from native HTML select element.'''
    start_time = time.time()

    # Select a country
    time.sleep(2)  # Slow down test execution
    selected = dropdown_page.select_country("United States")

    # Verify selection
    time.sleep(2)  # Slow down test execution
    assert selected == "United States"
    assert dropdown_page.verify_native_selection("United States")

    # Verify result displayed
    time.sleep(2)  # Wait for JS to update and slow down
    result_text = dropdown_page.get_native_result()
    assert "United States" in result_text

    # Add delay to reach ~10 seconds
    time.sleep(4)

    duration = time.time() - start_time
    print(f"\n✓ Native dropdown test completed in {duration:.2f}s")
    assert duration >= 8.0 and duration <= 14.0, f"Test duration {duration:.2f}s should be around 10 seconds"


def test_custom_dropdown_selection(dropdown_page):
    '''Test selecting from custom div-based dropdown.'''
    start_time = time.time()

    # Select an option
    time.sleep(2)  # Slow down test execution
    selected = dropdown_page.select_custom_option("Option 2")

    # Verify selection
    time.sleep(2)  # Slow down test execution
    assert selected == "Option 2"
    assert dropdown_page.verify_custom_selection("Option 2")

    # Verify result displayed
    time.sleep(2)  # Wait for JS to update and slow down
    result_text = dropdown_page.get_custom_result()
    assert "Option 2" in result_text

    # Add delay to reach ~10 seconds
    time.sleep(4)

    duration = time.time() - start_time
    print(f"\n✓ Custom dropdown test completed in {duration:.2f}s")
    assert duration >= 8.0 and duration <= 14.0, f"Test duration {duration:.2f}s should be around 10 seconds"


def test_multiple_selections(dropdown_page):
    '''Test multiple sequential selections to verify state management.'''
    start_time = time.time()

    # Native dropdown
    time.sleep(1.5)  # Slow down test execution
    dropdown_page.select_country("Canada")
    time.sleep(1)  # Slow down test execution
    assert dropdown_page.verify_native_selection("Canada")

    time.sleep(1.5)  # Slow down test execution
    dropdown_page.select_country("Germany")
    time.sleep(1)  # Slow down test execution
    assert dropdown_page.verify_native_selection("Germany")

    # Custom dropdown
    time.sleep(1.5)  # Slow down test execution
    dropdown_page.select_custom_option("Option 1")
    time.sleep(1)  # Slow down test execution
    assert dropdown_page.verify_custom_selection("Option 1")

    time.sleep(1.5)  # Slow down test execution
    dropdown_page.select_custom_option("Option 5")
    time.sleep(1)  # Slow down test execution
    assert dropdown_page.verify_custom_selection("Option 5")

    duration = time.time() - start_time
    print(f"\n✓ Multiple selections test passed in {duration:.2f}s")
    assert duration >= 8.0 and duration <= 14.0, f"Test duration {duration:.2f}s should be around 10 seconds"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
