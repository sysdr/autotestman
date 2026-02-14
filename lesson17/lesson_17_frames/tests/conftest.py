
"""
Pytest configuration and fixtures for frame testing
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pathlib import Path


@pytest.fixture(scope="function")
def driver():
    """
    Create a Chrome WebDriver instance for each test.
    Automatically cleans up after test completion.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(0)  # Disable implicit waits, use explicit only

    yield driver

    # Cleanup
    driver.quit()


@pytest.fixture(autouse=True)
def reset_frame_context(driver):
    """
    Automatically reset frame context after each test.
    Prevents context pollution between tests.
    """
    yield
    # This runs after each test
    driver.switch_to.default_content()


@pytest.fixture(scope="session")
def test_page_url():
    """Return file:// URL for local test page"""
    html_file = Path(__file__).parent.parent / "resources" / "test_frames.html"
    return f"file://{html_file.absolute()}"
