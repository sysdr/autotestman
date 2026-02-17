"""
Login Page Object
Demonstrates BasePage inheritance
"""

from core.base_page import BasePage
from selenium.webdriver.common.by import By
from typing import Tuple


class LoginPage(BasePage):
    """Login page object using BasePage methods"""
    
    # Locators as class constants
    USERNAME_INPUT: Tuple[str, str] = (By.ID, "username")
    PASSWORD_INPUT: Tuple[str, str] = (By.ID, "password")
    FORM: Tuple[str, str] = (By.TAG_NAME, "form")
    ERROR_MSG: Tuple[str, str] = (By.CSS_SELECTOR, "#flash")
    
    def login(self, username: str, password: str):
        """
        Perform login action
        
        Args:
            username: Username to enter
            password: Password to enter
        """
        self._type(self.USERNAME_INPUT, username)
        self._type(self.PASSWORD_INPUT, password)
        self._find(self.FORM).submit()
    
    def get_error_message(self) -> str:
        """Get error message text if displayed"""
        return self._get_text(self.ERROR_MSG)
    
    def is_error_displayed(self) -> bool:
        """Check if error message is displayed"""
        return self._is_displayed(self.ERROR_MSG)
