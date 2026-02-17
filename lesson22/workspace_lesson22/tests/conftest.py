"""
Pytest fixtures for tests
Uses system ChromeDriver  .
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# Use system chromedriver (e.g. /usr/bin/chromedriver); no third-party manager
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"


@pytest.fixture
def driver():
    """Create and teardown Chrome driver using system ChromeDriver"""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    service = Service(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(0)  # We use explicit waits only

    yield driver

    driver.quit()
