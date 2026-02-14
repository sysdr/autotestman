"""
conftest.py - Pytest configuration and fixtures
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pathlib import Path


@pytest.fixture(scope="function")
def chrome_driver():
    """Create a Chrome WebDriver instance"""
    options = Options()
    options.add_argument("--headless")  # Run in headless mode for CI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(2)  # 2 second implicit wait
    
    yield driver
    
    driver.quit()


@pytest.fixture(scope="session")
def test_page_url():
    """Get the absolute path to the test HTML file"""
    html_file = Path(__file__).parent.parent / "html" / "test_page.html"
    return f"file://{html_file.absolute()}"
