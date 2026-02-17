"""
Test Suite: Login Functionality
Demonstrates Page Object Model implementation
"""

import pytest
from pages.login_page import LoginPage


class TestLogin:
    """Test cases for login functionality using POM."""
    
    def test_successful_login_standard_user(self, driver):
        """
        Test successful login with standard user credentials.
        
        Verifies:
        - User can login with valid credentials
        - Products page loads after login
        - Correct page title is displayed
        """
        # Arrange
        login_page = LoginPage(driver)
        login_page.navigate_to()
        
        # Act
        products_page = login_page.login(
            username="standard_user",
            password="secret_sauce"
        )
        
        # Assert
        assert products_page.is_loaded(), "Products page should be loaded"
        assert products_page.get_page_title() == "Products",             "Page title should be 'Products'"
        assert products_page.get_product_count() > 0,             "Products should be displayed"
    
    def test_successful_login_with_fluent_api(self, driver):
        """
        Test login using fluent API (method chaining).
        
        Demonstrates alternative syntax for page object methods.
        """
        # Arrange & Act
        login_page = (
            LoginPage(driver)
            .navigate_to()
            .enter_username("standard_user")
            .enter_password("secret_sauce")
        )
        login_page.click_login_button()
        
        # Wait for navigation to products page
        login_page.wait_for_url_contains("inventory.html")
        from pages.products_page import ProductsPage
        products_page = ProductsPage(driver)
        
        # Assert
        assert products_page.is_loaded()
    
    def test_login_with_invalid_username(self, driver):
        """
        Test login failure with invalid username.
        
        Verifies:
        - Error message is displayed
        - User remains on login page
        - Error message contains expected text
        """
        # Arrange
        login_page = LoginPage(driver)
        login_page.navigate_to()
        
        # Act
        login_page.login_with_invalid_credentials(
            username="invalid_user",
            password="secret_sauce"
        )
        
        # Assert
        assert login_page.is_error_displayed(),             "Error message should be displayed"
        error_message = login_page.get_error_message()
        assert "Epic sadface" in error_message,             "Error message should contain 'Epic sadface'"
        assert "do not match" in error_message,             "Error should indicate credentials don't match"
    
    def test_login_with_invalid_password(self, driver):
        """Test login failure with invalid password."""
        login_page = LoginPage(driver)
        login_page.navigate_to()
        
        login_page.login_with_invalid_credentials(
            username="standard_user",
            password="wrong_password"
        )
        
        assert login_page.is_error_displayed()
    
    def test_login_with_empty_credentials(self, driver):
        """Test login failure with empty credentials."""
        login_page = LoginPage(driver)
        login_page.navigate_to()
        
        login_page.login_with_invalid_credentials("", "")
        
        assert login_page.is_error_displayed()
        error_message = login_page.get_error_message()
        assert "Username is required" in error_message
    
    def test_login_with_locked_user(self, driver):
        """
        Test login with locked out user.
        
        Verifies system handles locked accounts properly.
        """
        login_page = LoginPage(driver)
        login_page.navigate_to()
        
        login_page.login_with_invalid_credentials(
            username="locked_out_user",
            password="secret_sauce"
        )
        
        assert login_page.is_error_displayed()
        error_message = login_page.get_error_message()
        assert "locked out" in error_message.lower()


# Standalone test for demonstration
def test_login_page_loads_correctly(driver):
    """
    Test that login page loads with all required elements.
    
    This is a smoke test to verify page accessibility.
    """
    login_page = LoginPage(driver)
    login_page.navigate_to()
    
    assert login_page.is_loaded(), "Login page should load successfully"
    assert "Swag Labs" in driver.title, "Page title should contain 'Swag Labs'"
