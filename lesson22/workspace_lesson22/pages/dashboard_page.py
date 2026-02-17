"""
Dashboard Page Object
"""

from core.base_page import BasePage
from selenium.webdriver.common.by import By
from typing import Tuple


class DashboardPage(BasePage):
    """Dashboard page after login"""
    
    WELCOME_MSG: Tuple[str, str] = (By.CSS_SELECTOR, ".welcome-message")
    PROFILE_LINK: Tuple[str, str] = (By.ID, "profile-link")
    LOGOUT_BTN: Tuple[str, str] = (By.ID, "logout")
    
    def get_welcome_message(self) -> str:
        """Get welcome message text"""
        return self._get_text(self.WELCOME_MSG)
    
    def click_profile(self):
        """Navigate to profile page"""
        self._click(self.PROFILE_LINK)
    
    def logout(self):
        """Perform logout"""
        self._click(self.LOGOUT_BTN)
