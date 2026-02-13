"""
pages/login_page.py
Page Object Model for login functionality.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from utils.interactions import type_text, click_element, wait_for_text_in_element


class LoginPage:
    """
    Encapsulates login page structure and behaviors.

    Locators are defined as class attributes for easy modification.
    Methods represent user actions (login, logout) not implementation details.
    """

    # Locators
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    SUBMIT_BUTTON = (By.ID, "submit-btn")
    ERROR_MESSAGE = (By.ID, "error-msg")
    SUCCESS_MESSAGE = (By.ID, "success-msg")

    def __init__(self, driver: WebDriver, base_url: str = "http://localhost:8000"):
        """
        Initialize page object.

        Args:
            driver: WebDriver instance
            base_url: Base URL of application
        """
        self.driver = driver
        self.base_url = base_url

    def navigate(self) -> None:
        """Navigate to login page."""
        self.driver.get(f"{self.base_url}/login.html")
        print(f"  ✓ Navigated to {self.base_url}/login.html")

    def login(self, username: str, password: str) -> None:
        """
        Perform login action.

        Args:
            username: Username to enter
            password: Password to enter
        """
        print(f"\nAttempting login as '{username}'...")
        type_text(self.driver, self.USERNAME_FIELD, username)
        type_text(self.driver, self.PASSWORD_FIELD, password)
        click_element(self.driver, self.SUBMIT_BUTTON)

    def is_login_successful(self, timeout: int = 5) -> bool:
        """Check if login succeeded by waiting for success message."""
        return wait_for_text_in_element(
            self.driver, 
            self.SUCCESS_MESSAGE, 
            "Login successful!", 
            timeout
        )

    def get_error_message(self, timeout: int = 5) -> str:
        """Retrieve error message text if present."""
        try:
            from utils.interactions import safe_find_element
            element = safe_find_element(self.driver, self.ERROR_MESSAGE, timeout)
            return element.text
        except:
            return ""