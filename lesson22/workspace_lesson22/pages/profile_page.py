"""
Profile Page Object
"""

from core.base_page import BasePage
from selenium.webdriver.common.by import By
from typing import Tuple


class ProfilePage(BasePage):
    """User profile page"""
    
    PROFILE_NAME: Tuple[str, str] = (By.ID, "profile-name")
    EMAIL_FIELD: Tuple[str, str] = (By.ID, "email")
    SAVE_BTN: Tuple[str, str] = (By.ID, "save-profile")
    SUCCESS_MSG: Tuple[str, str] = (By.CSS_SELECTOR, ".success-message")
    
    def get_profile_name(self) -> str:
        """Get displayed profile name"""
        return self._get_text(self.PROFILE_NAME)
    
    def update_email(self, new_email: str):
        """Update email address"""
        self._type(self.EMAIL_FIELD, new_email)
        self._click(self.SAVE_BTN)
    
    def get_success_message(self) -> str:
        """Get success message after save"""
        return self._get_text(self.SUCCESS_MSG)
