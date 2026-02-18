"""Login Page Object"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import allure


class LoginPage(BasePage):
    """Page Object for login functionality"""
    
    # Locators (the-internet.herokuapp.com/login: form has username, password, and button.radius type=submit — no id on button)
    USERNAME_FIELD = (By.ID, "username")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CLASS_NAME, "flash")
    
    @allure.step("Perform login with username: {username}")
    def login(self, username: str, password: str) -> None:
        """Execute login flow"""
        self.enter_text(self.USERNAME_FIELD, username)
        self.enter_text(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BUTTON)
    
    @allure.step("Check if error message is displayed")
    def get_error_message(self) -> str:
        """Get error message text"""
        return self.find_element(self.ERROR_MESSAGE).text
