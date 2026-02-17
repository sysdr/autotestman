"""
BasePage: Foundation class for all Page Objects
Provides common utilities for element interactions and waits
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import Tuple


class BasePage:
    """Base class for all page objects. Provides common functionality."""
    
    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        Initialize BasePage.
        
        Args:
            driver: Selenium WebDriver instance
            timeout: Default timeout for waits (seconds)
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def find_element(self, locator: Tuple[str, str]) -> WebElement:
        """
        Find element with explicit wait (presence in DOM).
        
        Args:
            locator: Tuple of (By strategy, locator string)
            
        Returns:
            WebElement instance
            
        Raises:
            TimeoutException: If element not found within timeout
        """
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(
                f"Element {locator} not found after {self.timeout} seconds"
            )

    def wait_for_element_visible(self, locator: Tuple[str, str], timeout: int = None) -> WebElement:
        """
        Wait for element to be visible (present in DOM and displayed).
        Preferred for "page ready" checks and before interaction.
        
        Args:
            locator: Tuple of (By strategy, locator string)
            timeout: Optional custom timeout (uses default if None)
            
        Returns:
            WebElement instance
            
        Raises:
            TimeoutException: If element not visible within timeout
        """
        wait_timeout = timeout if timeout is not None else self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        try:
            return wait.until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(
                f"Element {locator} not visible after {wait_timeout} seconds"
            )
    
    def find_elements(self, locator: Tuple[str, str]) -> list[WebElement]:
        """
        Find multiple elements with explicit wait.
        
        Args:
            locator: Tuple of (By strategy, locator string)
            
        Returns:
            List of WebElement instances
        """
        self.find_element(locator)  # Wait for at least one element
        return self.driver.find_elements(*locator)
    
    def click(self, locator: Tuple[str, str]) -> None:
        """
        Click element with explicit wait for clickability.
        
        Args:
            locator: Tuple of (By strategy, locator string)
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def type_text(self, locator: Tuple[str, str], text: str, clear_first: bool = True) -> None:
        """
        Type text into input field.
        
        Args:
            locator: Tuple of (By strategy, locator string)
            text: Text to type
            clear_first: Whether to clear field before typing
        """
        element = self.find_element(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def get_text(self, locator: Tuple[str, str]) -> str:
        """
        Get text content of element.
        
        Args:
            locator: Tuple of (By strategy, locator string)
            
        Returns:
            Text content of element
        """
        element = self.find_element(locator)
        return element.text
    
    def is_element_visible(self, locator: Tuple[str, str]) -> bool:
        """
        Check if element is visible.
        
        Args:
            locator: Tuple of (By strategy, locator string)
            
        Returns:
            True if element is visible, False otherwise
        """
        try:
            element = self.find_element(locator)
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False
    
    def wait_for_url_contains(self, url_fragment: str, timeout: int = None) -> bool:
        """
        Wait for URL to contain specific fragment.
        
        Args:
            url_fragment: String that should be in URL
            timeout: Custom timeout (uses default if None)
            
        Returns:
            True if URL contains fragment within timeout
        """
        wait_timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, wait_timeout)
        return wait.until(EC.url_contains(url_fragment))
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.driver.current_url
    
    def get_page_title(self) -> str:
        """Get current page title"""
        return self.driver.title
