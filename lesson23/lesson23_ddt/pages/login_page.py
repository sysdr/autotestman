"""
Login Page Object - Encapsulates login page interactions
Demonstrates Page Object Model pattern for maintainability.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class LoginPage:
    """Page Object for login functionality"""
    
    # Locators as class constants
    EMAIL_INPUT = (By.ID, "email")
    PASSWORD_INPUT = (By.ID, "password")
    SUBMIT_BUTTON = (By.ID, "login-btn")
    DASHBOARD_HEADER = (By.CSS_SELECTOR, "h1.dashboard-title")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-msg")
    
    def __init__(self, driver, timeout: int = 10):
        """
        Initialize page object with WebDriver instance.
        
        Args:
            driver: Selenium WebDriver instance
            timeout: Default wait timeout in seconds
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
    
    def navigate_to_login(self, url: str = "https://demo.testcompany.com/login"):
        """Navigate to login page"""
        self.driver.get(url)
        return self
    
    def enter_email(self, email: str):
        """Enter email address"""
        email_field = self.wait.until(
            EC.presence_of_element_located(self.EMAIL_INPUT)
        )
        email_field.clear()
        email_field.send_keys(email)
        return self
    
    def enter_password(self, password: str):
        """Enter password"""
        password_field = self.wait.until(
            EC.presence_of_element_located(self.PASSWORD_INPUT)
        )
        password_field.clear()
        password_field.send_keys(password)
        return self
    
    def click_submit(self):
        """Click login button"""
        submit_btn = self.wait.until(
            EC.element_to_be_clickable(self.SUBMIT_BUTTON)
        )
        submit_btn.click()
        return self
    
    def login(self, email: str, password: str):
        """
        Complete login flow (fluent interface pattern).
        
        Args:
            email: User email
            password: User password
        """
        self.enter_email(email).enter_password(password).click_submit()
        return self
    
    def get_dashboard_title(self) -> str:
        """Get dashboard header text after login"""
        try:
            header = self.wait.until(
                EC.presence_of_element_located(self.DASHBOARD_HEADER)
            )
            return header.text
        except TimeoutException:
            return ""
    
    def is_logged_in(self) -> bool:
        """Check if login was successful"""
        return len(self.get_dashboard_title()) > 0
    
    def get_error_message(self) -> str:
        """Get error message if login failed"""
        try:
            error = self.wait.until(
                EC.presence_of_element_located(self.ERROR_MESSAGE)
            )
            return error.text
        except TimeoutException:
            return ""
