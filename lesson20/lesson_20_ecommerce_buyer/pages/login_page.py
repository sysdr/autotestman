"""
LoginPage - Handles authentication
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for login functionality"""
    
    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    def login(self, username: str, password: str) -> None:
        """
        Perform login action
        
        Args:
            username: User credential
            password: User credential
        """
        self.wait_and_send_keys(self.USERNAME_INPUT, username)
        self.wait_and_send_keys(self.PASSWORD_INPUT, password)
        self.wait_and_click(self.LOGIN_BUTTON)
    
    def is_login_successful(self) -> bool:
        """Check if login was successful by checking URL"""
        return self.wait_for_url_contains("/inventory.html")
    
    def get_error_message(self) -> str:
        """Get error message if login fails"""
        return self.get_element_text(self.ERROR_MESSAGE)
