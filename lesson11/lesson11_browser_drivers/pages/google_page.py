"""
Google Home Page Object
Encapsulates navigation and assertions for google.com
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GoogleHomePage:
    """Page Object for Google homepage."""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.url = "https://www.google.com"
        self.timeout = 10
    
    def load(self) -> "GoogleHomePage":
        """
        Navigate to Google and wait for page to be ready.
        
        Returns:
            Self for method chaining
            
        Raises:
            TimeoutException: If page doesn't load within timeout
        """
        self.driver.get(self.url)
        
        # Explicit wait for page title to contain "Google"
        wait = WebDriverWait(self.driver, self.timeout)
        wait.until(EC.title_contains("Google"))
        
        return self
    
    def get_title(self) -> str:
        """
        Get the current page title.
        
        Returns:
            Page title as string
        """
        return self.driver.title
    
    def verify_loaded(self) -> bool:
        """
        Verify the page is properly loaded.
        
        Returns:
            True if title contains "Google"
        """
        return "Google" in self.driver.title
