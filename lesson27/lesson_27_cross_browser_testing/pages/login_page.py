"""
Login Page Object
=================
Page Object Model for the login page.
Browser-agnostic implementation.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage:
    """Page Object for login functionality."""
    
    # Locators - use cross-browser compatible selectors
    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    FLASH_MESSAGE = (By.ID, "flash")
    LOGOUT_BUTTON = (By.CSS_SELECTOR, "a[href='/logout']")
    
    def __init__(self, driver: WebDriver, timeout: int = 10):
        """Initialize the page object."""
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
    
    def _pause_after_action(self) -> None:
        """Pause after an action when --slow is used (so you can watch)."""
        delay = getattr(self.driver, "action_delay", 0)
        if delay > 0:
            time.sleep(delay)
    
    def navigate_to(self, base_url: str) -> None:
        """Navigate to the login page."""
        self.driver.get(f"{base_url}/login")
        self._pause_after_action()
    
    def enter_username(self, username: str) -> None:
        """Enter username."""
        element = self.wait.until(
            EC.presence_of_element_located(self.USERNAME_INPUT)
        )
        element.clear()
        element.send_keys(username)
        self._pause_after_action()
    
    def enter_password(self, password: str) -> None:
        """Enter password."""
        element = self.wait.until(
            EC.presence_of_element_located(self.PASSWORD_INPUT)
        )
        element.clear()
        element.send_keys(password)
        self._pause_after_action()
    
    def click_login(self) -> None:
        """Click the login button."""
        element = self.wait.until(
            EC.element_to_be_clickable(self.LOGIN_BUTTON)
        )
        element.click()
        self._pause_after_action()
    
    def login(self, username: str, password: str) -> None:
        """Complete login flow."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
    
    def get_flash_message(self) -> str:
        """Get the flash message text."""
        element = self.wait.until(
            EC.visibility_of_element_located(self.FLASH_MESSAGE)
        )
        return element.text
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in."""
        try:
            self.wait.until(
                EC.presence_of_element_located(self.LOGOUT_BUTTON)
            )
            return True
        except:
            return False
