"""
Driver Manager: WebDriver setup and teardown utilities
Handles browser initialization with optimal settings
"""

import os
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def create_chrome_driver(headless: bool = False) -> webdriver.Chrome:
    """
    Create and configure Chrome WebDriver.
    
    Args:
        headless: Whether to run browser in headless mode
        
    Returns:
        Configured Chrome WebDriver instance
    """
    options = Options()
    
    # Performance optimizations
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-popup-blocking')
    
    # Headless mode for CI/CD
    if headless:
        options.add_argument('--headless=new')
    
    # Window size for consistent screenshots
    options.add_argument('--window-size=1920,1080')
    
    # Initialize driver with webdriver-manager (auto-downloads correct chromedriver)
    # Workaround: ChromeDriverManager can return THIRD_PARTY_NOTICES.chromedriver path (known bug)
    driver_path = ChromeDriverManager().install()
    if driver_path:
        path = Path(driver_path)
        if path.name != "chromedriver":
            driver_path = str(path.parent / "chromedriver")
        if os.path.isfile(driver_path):
            os.chmod(driver_path, 0o755)
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    # Implicit wait as fallback (prefer explicit waits in page objects)
    driver.implicitly_wait(2)
    
    return driver
