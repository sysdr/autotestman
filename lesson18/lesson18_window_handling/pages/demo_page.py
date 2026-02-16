"""
Page Object Model for Window Handling Demo Page.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class DemoPage:
    """Page object for the window handling demo page."""
    
    # Locators
    OPEN_TAB_LINK = (By.ID, "open-tab")
    OPEN_WINDOW_LINK = (By.ID, "open-window")
    PAGE_TITLE = (By.TAG_NAME, "h1")
    
    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        Initialize page object.
        
        Args:
            driver: Selenium WebDriver instance
            timeout: Default timeout for waits
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
    
    def load(self, url: str) -> None:
        """Load the demo page."""
        self.driver.get(url)
        self.wait.until(EC.presence_of_element_located(self.PAGE_TITLE))
    
    def click_open_tab_link(self) -> None:
        """Click the link that opens a new tab."""
        element: WebElement = self.wait.until(
            EC.element_to_be_clickable(self.OPEN_TAB_LINK)
        )
        element.click()
    
    def click_open_window_link(self) -> None:
        """Click the link that opens a new window."""
        element: WebElement = self.wait.until(
            EC.element_to_be_clickable(self.OPEN_WINDOW_LINK)
        )
        element.click()
    
    def get_page_title_text(self) -> str:
        """Get the text of the page title."""
        element: WebElement = self.wait.until(
            EC.presence_of_element_located(self.PAGE_TITLE)
        )
        return element.text
    
    @property
    def current_url(self) -> str:
        """Get current URL."""
        return self.driver.current_url
