"""
conftest.py
Pytest fixtures for WebDriver management.
"""

import os
from pathlib import Path
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    """
    Provides a Chrome WebDriver instance for each test.

    Automatically:
    - Downloads correct ChromeDriver version
    - Configures headless mode for CI
    - Cleans up after test completes
    """
    options = Options()
    # Uncomment for headless execution in CI
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # Fix ChromeDriver path - ensure we get the actual executable
    driver_path = ChromeDriverManager().install()
    # If the path points to a directory, find the chromedriver executable
    if os.path.isdir(driver_path):
        driver_path = os.path.join(driver_path, "chromedriver")
    # If it points to a wrong file, find the correct one in the parent directory
    elif "THIRD_PARTY_NOTICES" in driver_path or not os.path.isfile(driver_path):
        driver_dir = os.path.dirname(driver_path)
        driver_path = os.path.join(driver_dir, "chromedriver")
        if not os.path.exists(driver_path):
            # Try parent directory
            parent_dir = os.path.dirname(driver_dir)
            driver_path = os.path.join(parent_dir, "chromedriver")
    
    # Make sure it's executable
    if os.path.exists(driver_path):
        os.chmod(driver_path, 0o755)
    
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(0)  # Force explicit waits only

    yield driver

    driver.quit()