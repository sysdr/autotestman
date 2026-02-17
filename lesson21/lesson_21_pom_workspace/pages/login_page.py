"""
LoginPage: Page Object for login functionality
Encapsulates all interactions with the login page
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pages.products_page import ProductsPage


class LoginPage(BasePage):
    """Page Object representing the login page."""
    
    # Locators - centralized for easy maintenance
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    ERROR_BUTTON = (By.CSS_SELECTOR, ".error-button")
    
    # Page URL
    URL = "https://www.saucedemo.com"
    
    def __init__(self, driver: WebDriver):
        """Initialize LoginPage"""
        super().__init__(driver)
    
    def navigate_to(self) -> 'LoginPage':
        """
        Navigate to login page and wait until it is fully loaded and ready for interaction.
        Ensures correct URL and visible login form (POM best practice: explicit visibility wait).
        
        Returns:
            Self for method chaining
        """
        self.driver.get(self.URL)
        # Ensure we are on the login page (handles redirects/slow load)
        self.wait_for_url_contains("saucedemo.com")
        # Wait for login form to be visible (preferred over presence for interaction readiness)
        self.wait_for_element_visible(self.USERNAME_INPUT)
        return self
    
    def enter_username(self, username: str) -> 'LoginPage':
        """
        Enter username into username field.
        
        Args:
            username: Username to enter
            
        Returns:
            Self for method chaining (Fluent API)
        """
        self.type_text(self.USERNAME_INPUT, username)
        return self
    
    def enter_password(self, password: str) -> 'LoginPage':
        """
        Enter password into password field.
        
        Args:
            password: Password to enter
            
        Returns:
            Self for method chaining
        """
        self.type_text(self.PASSWORD_INPUT, password)
        return self
    
    def click_login_button(self) -> None:
        """Click the login button."""
        self.click(self.LOGIN_BUTTON)
    
    def login(self, username: str, password: str) -> 'ProductsPage':
        """
        Complete login flow with valid credentials.
        
        This is the primary method tests should use.
        It performs the full login sequence and returns the next page.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            ProductsPage instance (next page in flow)
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        
        # Wait for navigation to products page
        self.wait_for_url_contains("inventory.html")
        
        # Import here to avoid circular dependency
        from pages.products_page import ProductsPage
        return ProductsPage(self.driver)
    
    def login_with_invalid_credentials(self, username: str, password: str) -> 'LoginPage':
        """
        Attempt login with invalid credentials.
        
        Used for negative test cases. Remains on login page.
        
        Args:
            username: Invalid username
            password: Invalid password
            
        Returns:
            Self (stays on login page)
        """
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        return self
    
    def get_error_message(self) -> str:
        """
        Get error message text.
        
        Returns:
            Error message text
        """
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_displayed(self) -> bool:
        """
        Check if error message is displayed.
        
        Returns:
            True if error is visible
        """
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def is_loaded(self) -> bool:
        """
        Verify login page is loaded.
        
        Returns:
            True if login page is loaded
        """
        return (
            self.is_element_visible(self.USERNAME_INPUT) and
            self.is_element_visible(self.PASSWORD_INPUT) and
            self.is_element_visible(self.LOGIN_BUTTON)
        )
