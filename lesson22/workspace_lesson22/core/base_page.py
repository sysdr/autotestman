"""
Base Page: Foundation for all Page Objects
Provides generic methods: find, click, type with built-in waits
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Tuple
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BasePage:
    """Abstract base class for all page objects"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
    def _find(self, locator: Tuple[str, str]):
        """
        Find element with explicit wait
        
        Args:
            locator: Tuple of (By strategy, locator string)
            
        Returns:
            WebElement when found
            
        Raises:
            TimeoutException: If element not found within timeout
        """
        try:
            element = self.wait.until(
                EC.presence_of_element_located(locator)
            )
            logger.info(f"✓ Found element: {locator}")
            return element
        except TimeoutException:
            logger.error(f"✗ Timeout finding element: {locator}")
            self._take_screenshot(f"timeout_{locator[1]}")
            raise
    
    def _click(self, locator: Tuple[str, str]):
        """
        Click element with auto-wait
        
        Args:
            locator: Tuple of (By strategy, locator string)
        """
        element = self._find(locator)
        element.click()
        logger.info(f"✓ Clicked: {locator}")
    
    def _type(self, locator: Tuple[str, str], text: str, clear_first: bool = True):
        """
        Type text into element with auto-wait
        
        Args:
            locator: Tuple of (By strategy, locator string)
            text: Text to type
            clear_first: Whether to clear field first
        """
        element = self._find(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        logger.info(f"✓ Typed '{text}' into: {locator}")
    
    def _get_text(self, locator: Tuple[str, str]) -> str:
        """
        Get element text with auto-wait (waits for visibility so text is rendered).
        
        Args:
            locator: Tuple of (By strategy, locator string)
            
        Returns:
            Element text content
        """
        try:
            element = self.wait.until(
                EC.visibility_of_element_located(locator)
            )
        except TimeoutException:
            logger.error(f"✗ Timeout waiting for element visible: {locator}")
            self._take_screenshot(f"timeout_visible_{locator[1]}")
            raise
        text = element.text
        logger.info(f"✓ Got text '{text}' from: {locator}")
        return text
    
    def _is_displayed(self, locator: Tuple[str, str]) -> bool:
        """
        Check if element is displayed
        
        Args:
            locator: Tuple of (By strategy, locator string)
            
        Returns:
            True if element is displayed
        """
        try:
            element = self._find(locator)
            return element.is_displayed()
        except TimeoutException:
            return False
    
    def _take_screenshot(self, name: str):
        """
        Take screenshot for debugging
        
        Args:
            name: Screenshot file name
        """
        screenshots_dir = Path("screenshots")
        screenshots_dir.mkdir(exist_ok=True)
        filepath = screenshots_dir / f"{name}.png"
        self.driver.save_screenshot(str(filepath))
        logger.info(f"📸 Screenshot saved: {filepath}")
