"""
BasePage - Foundation for all Page Objects
Provides reusable wait mechanisms and common operations
"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException
from selenium.webdriver.common.alert import Alert
from typing import Tuple
import time


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.timeout = timeout
    
    def wait_and_find(self, locator: Tuple[str, str]) -> WebElement:
        """
        Wait for element to be present in DOM
        
        Args:
            locator: Tuple of (By.X, "selector")
        
        Returns:
            WebElement when found
        
        Raises:
            TimeoutException: If element not found within timeout
        """
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(
                f"Element not found within {self.timeout}s: {locator}"
            )
    
    def wait_and_click(self, locator: Tuple[str, str]) -> WebElement:
        """
        Wait for element to be clickable, then click it
        
        This checks:
        - Element is present in DOM
        - Element is visible
        - Element is enabled
        - Element is not obscured
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            return element
        except TimeoutException:
            raise TimeoutException(
                f"Element not clickable within {self.timeout}s: {locator}"
            )
    
    def wait_and_send_keys(
        self, 
        locator: Tuple[str, str], 
        text: str,
        clear_first: bool = True
    ) -> WebElement:
        """
        Wait for element to be present, optionally clear it, then send keys
        """
        element = self.wait_and_find(locator)
        
        if clear_first:
            element.clear()
        
        element.send_keys(text)
        return element
    
    def wait_for_url_contains(self, url_fragment: str) -> bool:
        """Wait for URL to contain specific fragment"""
        try:
            self.wait.until(EC.url_contains(url_fragment))
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_text(
        self, 
        locator: Tuple[str, str], 
        expected_text: str
    ) -> bool:
        """Wait for element to contain specific text"""
        try:
            self.wait.until(
                EC.text_to_be_present_in_element(locator, expected_text)
            )
            return True
        except TimeoutException:
            return False
    
    def get_element_text(self, locator: Tuple[str, str]) -> str:
        """Get text content of element"""
        element = self.wait_and_find(locator)
        return element.text
    
    def is_element_visible(self, locator: Tuple[str, str]) -> bool:
        """Check if element is visible without waiting"""
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except:
            return False
    
    def handle_alert(self, accept: bool = True) -> str:
        """
        Handle browser alert/authentication dialog automatically
        
        Args:
            accept: If True, accept the alert. If False, dismiss it.
        
        Returns:
            Alert text if alert was present, empty string otherwise
        """
        try:
            alert = Alert(self.driver)
            alert_text = alert.text
            if accept:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        except NoAlertPresentException:
            return ""
    
    def wait_and_click_with_alert_handling(self, locator: Tuple[str, str]) -> WebElement:
        """
        Wait for element to be clickable, click it, and handle any alerts that appear
        
        This is useful for buttons that trigger browser security dialogs
        """
        element = self.wait_and_click(locator)
        # Check for and handle any alerts that might appear after clicking
        time.sleep(0.5)  # Brief wait for alert to appear
        self.handle_alert(accept=True)
        return element