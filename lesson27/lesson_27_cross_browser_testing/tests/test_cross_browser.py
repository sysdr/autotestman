"""
Chrome Test Suite
==================
Tests that run on Chrome.
"""

import time
import pytest
from pages.login_page import LoginPage


class TestCrossBrowserLogin:
    """Test login functionality on Chrome."""
    
    def test_successful_login(self, browser, base_url):
        """
        Test successful login flow on Chrome.
        """
        print(f"\n▶️  Running on {browser.browser_name.upper()}")
        
        # Initialize page object
        login_page = LoginPage(browser)
        
        # Navigate to login page
        login_page.navigate_to(base_url)
        
        # Perform login
        login_page.login(username="tomsmith", password="SuperSecretPassword!")
        
        # Verify success
        assert login_page.is_logged_in(), "Login failed - user not logged in"
        
        flash_message = login_page.get_flash_message()
        assert "You logged into a secure area!" in flash_message,             f"Unexpected flash message: {flash_message}"
        
        print(f"✅ Login successful on {browser.browser_name.upper()}")
    
    def test_failed_login(self, browser, base_url):
        """Test login with invalid credentials."""
        print(f"\n▶️  Running on {browser.browser_name.upper()}")
        
        login_page = LoginPage(browser)
        login_page.navigate_to(base_url)
        
        # Attempt login with wrong password
        login_page.login(username="tomsmith", password="wrongpassword")
        
        # Verify error message
        flash_message = login_page.get_flash_message()
        assert "Your password is invalid!" in flash_message,             f"Expected error message not found: {flash_message}"
        
        assert not login_page.is_logged_in(), "Should not be logged in"
        
        print(f"✅ Invalid login correctly rejected on {browser.browser_name.upper()}")
    
    def test_empty_credentials(self, browser, base_url):
        """Test login with empty credentials."""
        print(f"\n▶️  Running on {browser.browser_name.upper()}")
        
        login_page = LoginPage(browser)
        login_page.navigate_to(base_url)
        
        # Attempt login with empty fields
        login_page.login(username="", password="")
        
        # Verify error message
        flash_message = login_page.get_flash_message()
        assert "Your username is invalid!" in flash_message
        
        print(f"✅ Empty credentials correctly rejected on {browser.browser_name.upper()}")


class TestCrossBrowserNavigation:
    """Test navigation on Chrome."""
    
    def test_page_title(self, browser, base_url):
        """Verify page title on Chrome."""
        browser.get(f"{base_url}/login")
        if getattr(browser, "action_delay", 0) > 0:
            time.sleep(browser.action_delay)
        assert "The Internet" in browser.title
        print(f"✅ Page title verified on {browser.browser_name.upper()}")
    
    def test_page_elements_present(self, browser, base_url):
        """Verify all expected elements are present."""
        login_page = LoginPage(browser)
        login_page.navigate_to(base_url)
        
        # Verify key elements exist
        from selenium.webdriver.support import expected_conditions as EC
        
        assert login_page.wait.until(
            EC.presence_of_element_located(login_page.USERNAME_INPUT)
        )
        assert login_page.wait.until(
            EC.presence_of_element_located(login_page.PASSWORD_INPUT)
        )
        assert login_page.wait.until(
            EC.presence_of_element_located(login_page.LOGIN_BUTTON)
        )
        
        print(f"✅ All elements present on {browser.browser_name.upper()}")
