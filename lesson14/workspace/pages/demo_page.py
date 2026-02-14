"""
demo_page.py - Page Object Model for the demo page
"""

from enum import Enum
from dataclasses import dataclass
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from typing import Tuple
import time


class LocatorType(Enum):
    """Available locator strategies"""
    ID = "id"
    CLASS = "class_name"
    CSS = "css_selector"
    XPATH = "xpath"


@dataclass
class LocatorStrategy:
    """Represents a locator strategy with metadata"""
    name: str
    type: LocatorType
    value: str
    description: str
    risk_level: str  # "LOW", "MEDIUM", "HIGH"
    
    def to_selenium_tuple(self) -> Tuple[str, str]:
        """Convert to Selenium By tuple"""
        by_mapping = {
            LocatorType.ID: By.ID,
            LocatorType.CLASS: By.CLASS_NAME,
            LocatorType.CSS: By.CSS_SELECTOR,
            LocatorType.XPATH: By.XPATH,
        }
        return (by_mapping[self.type], self.value)


class DemoPage:
    """Page Object for the locator strategy demo page"""
    
    # Define all locator strategies for the submit button
    LOCATORS = {
        "by_id": LocatorStrategy(
            name="By ID",
            type=LocatorType.ID,
            value="submit-btn",
            description="Fastest and most resilient strategy",
            risk_level="LOW"
        ),
        "by_class": LocatorStrategy(
            name="By Class",
            type=LocatorType.CLASS,
            value="btn-primary",
            description="Risky if class is reused elsewhere",
            risk_level="MEDIUM"
        ),
        "by_css_attribute": LocatorStrategy(
            name="By CSS (data-testid)",
            type=LocatorType.CSS,
            value="button[data-testid='submit-button']",
            description="Semantic and stable with test IDs",
            risk_level="LOW"
        ),
        "by_xpath_text": LocatorStrategy(
            name="By XPath (text content)",
            type=LocatorType.XPATH,
            value="//button[contains(text(), 'Submit Order')]",
            description="Useful when only text is unique",
            risk_level="MEDIUM"
        ),
        "by_xpath_absolute": LocatorStrategy(
            name="By XPath (absolute path)",
            type=LocatorType.XPATH,
            value="/html/body/div/button",
            description="ANTI-PATTERN: Breaks with any DOM change",
            risk_level="HIGH"
        ),
    }
    
    def __init__(self, driver: WebDriver, url: str):
        """Initialize page object with driver and URL"""
        self.driver = driver
        self.url = url
    
    def load(self):
        """Load the page"""
        self.driver.get(self.url)
    
    def find_button_with_strategy(self, strategy_key: str) -> Tuple[WebElement, float]:
        """
        Find button using specified strategy and measure time
        
        Returns:
            Tuple of (WebElement, execution_time_in_seconds)
        """
        strategy = self.LOCATORS[strategy_key]
        by_type, by_value = strategy.to_selenium_tuple()
        
        start_time = time.time()
        element = self.driver.find_element(by_type, by_value)
        elapsed_time = time.time() - start_time
        
        return element, elapsed_time
    
    def click_button_with_strategy(self, strategy_key: str) -> float:
        """Click button using specified strategy and return execution time"""
        element, elapsed_time = self.find_button_with_strategy(strategy_key)
        element.click()
        return elapsed_time
    
    def verify_button_clicked(self) -> bool:
        """Verify the success message appears after clicking"""
        try:
            result_div = self.driver.find_element(By.ID, "result")
            return "success" in result_div.get_attribute("class")
        except:
            return False
