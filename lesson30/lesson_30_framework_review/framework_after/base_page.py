"""Base page class with type hints and comprehensive docstrings.

This module provides the foundation for all page objects in the UQAP framework.
All methods include type hints for static analysis and detailed docstrings
for maintainability.
"""

from typing import List, Optional, Tuple
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    """Base class for all page objects providing common web interactions.
    
    This class encapsulates Selenium WebDriver operations with type safety
    and explicit waits to ensure stability in CI/CD environments.
    
    Attributes:
        driver: Selenium WebDriver instance
        wait: Default WebDriverWait instance (10 second timeout)
    """
    
    def __init__(self, driver: webdriver.Remote) -> None:
        """Initialize base page with WebDriver instance.
        
        Args:
            driver: Selenium WebDriver instance for browser automation
        """
        self.driver: webdriver.Remote = driver
        self.wait: WebDriverWait = WebDriverWait(driver, 10)
    
    def find_element(self, locator: Tuple[str, str]) -> WebElement:
        """Find a single element immediately without waiting.
        
        Args:
            locator: Selenium locator tuple (By.ID, "element_id")
            
        Returns:
            WebElement instance if found
            
        Raises:
            NoSuchElementException: If element not found in DOM
        """
        return self.driver.find_element(*locator)
    
    def find_elements(self, locator: Tuple[str, str]) -> List[WebElement]:
        """Find all matching elements immediately without waiting.
        
        Args:
            locator: Selenium locator tuple (By.CLASS_NAME, "item")
            
        Returns:
            List of WebElement instances (empty list if none found)
        """
        return self.driver.find_elements(*locator)
    
    def click(self, locator: Tuple[str, str], timeout: int = 10) -> None:
        """Click an element after waiting for it to be clickable.
        
        Uses explicit wait to ensure element is both visible and enabled
        before attempting click. This prevents ElementNotInteractableException
        in dynamic web applications.
        
        Args:
            locator: Selenium locator tuple for target element
            timeout: Maximum seconds to wait for element (default: 10)
            
        Raises:
            TimeoutException: If element not clickable within timeout
        """
        element: WebElement = self.wait_for_clickable(locator, timeout)
        element.click()
    
    def send_keys(
        self, 
        locator: Tuple[str, str], 
        text: str, 
        clear_first: bool = True
    ) -> None:
        """Type text into an input element.
        
        Args:
            locator: Selenium locator tuple for input element
            text: Text string to type into element
            clear_first: Whether to clear existing text before typing
            
        Raises:
            NoSuchElementException: If input element not found
        """
        element: WebElement = self.find_element(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
    
    def wait_for_element(
        self, 
        locator: Tuple[str, str], 
        timeout: int = 10
    ) -> WebElement:
        """Wait for element to be present in the DOM.
        
        Element may not be visible but must exist in page structure.
        Use wait_for_clickable() if you need visible + enabled guarantee.
        
        Args:
            locator: Selenium locator tuple
            timeout: Maximum seconds to wait
            
        Returns:
            WebElement once present in DOM
            
        Raises:
            TimeoutException: If element not present within timeout
        """
        wait: WebDriverWait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    def wait_for_clickable(
        self, 
        locator: Tuple[str, str], 
        timeout: int = 10
    ) -> WebElement:
        """Wait for element to be visible and enabled for interaction.
        
        This is stricter than wait_for_element() - ensures element can
        actually be clicked/interacted with.
        
        Args:
            locator: Selenium locator tuple
            timeout: Maximum seconds to wait
            
        Returns:
            WebElement once clickable
            
        Raises:
            TimeoutException: If element not clickable within timeout
        """
        wait: WebDriverWait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def is_element_present(self, locator: Tuple[str, str]) -> bool:
        """Check if element exists in DOM without waiting.
        
        This is a non-blocking check useful for conditional logic.
        For waiting behavior, use wait_for_element() instead.
        
        Args:
            locator: Selenium locator tuple
            
        Returns:
            True if element found, False otherwise
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def get_text(self, locator: Tuple[str, str]) -> str:
        """Retrieve visible text content of an element.
        
        Args:
            locator: Selenium locator tuple
            
        Returns:
            Text content as string (empty string if no text)
            
        Raises:
            NoSuchElementException: If element not found
        """
        element: WebElement = self.find_element(locator)
        return element.text
    
    def get_attribute(
        self, 
        locator: Tuple[str, str], 
        attribute: str
    ) -> Optional[str]:
        """Get HTML attribute value from an element.
        
        Args:
            locator: Selenium locator tuple
            attribute: HTML attribute name (e.g., "href", "class", "data-id")
            
        Returns:
            Attribute value as string, or None if attribute doesn't exist
            
        Raises:
            NoSuchElementException: If element not found
        """
        element: WebElement = self.find_element(locator)
        return element.get_attribute(attribute)
