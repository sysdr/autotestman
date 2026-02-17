"""
Data-Driven Login Tests
Demonstrates pytest.mark.parametrize with external JSON data.
"""

import pytest
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from pages.login_page import LoginPage
from utils.data_loader import load_credentials, get_test_ids


@pytest.fixture(scope="function")
def browser():
    """
    Setup and teardown browser for each test.
    Scope='function' ensures each test gets a fresh browser.
    """
    # Setup: Create browser instance
    options = Options()
    options.add_argument("--headless")  # Run without GUI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    # Use system ChromeDriver (e.g. /usr/bin/chromedriver), no third-party driver manager
    service = Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    
    yield driver  # This is where the test runs
    
    # Teardown: Quit browser
    driver.quit()


# The DDT Magic: One test, multiple datasets
@pytest.mark.parametrize(
    "credentials",
    load_credentials(),  # Load all 5 credential sets
    ids=get_test_ids     # Use role names as test IDs
)
def test_login_with_different_roles(browser, login_base_url, credentials):
    """
    Test login functionality with different user roles.
    This single method runs 5 times, once for each credential set.
    
    Args:
        browser: WebDriver instance from fixture
        login_base_url: Local HTTP server URL (from conftest)
        credentials: Dict from JSON, injected by parametrize
    """
    # Arrange: Create page object and navigate to local mock login page
    login_page = LoginPage(browser)
    expected = credentials["expected_dashboard"]
    url = f"{login_base_url}/login.html?expected={quote(expected)}"
    login_page.navigate_to_login(url)
    
    # Act: Perform login
    login_page.login(
        email=credentials["email"],
        password=credentials["password"]
    )
    
    # Assert: Verify expected outcome
    actual_title = login_page.get_dashboard_title()
    expected_title = credentials["expected_dashboard"]
    
    assert actual_title == expected_title, (
        f"Login failed for {credentials['role']} user. "
        f"Expected: '{expected_title}', Got: '{actual_title}'"
    )
    
    # Additional assertion: Check if logged in
    assert login_page.is_logged_in(), (
        f"User {credentials['role']} is not logged in despite correct credentials"
    )


def test_data_loader_validation():
    """
    Sanity test: Verify data loader works correctly.
    This ensures our JSON file is valid and contains expected data.
    """
    credentials = load_credentials()
    
    # Should have exactly 5 credential sets
    assert len(credentials) == 5, f"Expected 5 credentials, got {len(credentials)}"
    
    # All should have required fields
    required_fields = ["role", "email", "password", "expected_dashboard"]
    for cred in credentials:
        for field in required_fields:
            assert field in cred, f"Missing field '{field}' in {cred.get('role', 'unknown')} credentials"
    
    # Roles should be unique
    roles = [cred["role"] for cred in credentials]
    assert len(roles) == len(set(roles)), "Duplicate roles found in credentials"


# Demonstration: Run tests programmatically
if __name__ == "__main__":
    """
    Run tests from command line for demo purposes.
    In production, use: pytest tests/test_ddt_login.py -v
    """
    import subprocess
    
    result = subprocess.run(
        ["pytest", __file__, "-v", "--tb=short"],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    print(result.stderr)
