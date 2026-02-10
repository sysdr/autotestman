"""
WebDriver Manager Utility
Handles driver initialization and teardown with proper resource management.
"""

from typing import Optional
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class DriverManager:
    """Manages WebDriver lifecycle."""
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.driver: Optional[webdriver.Chrome] = None
    
    def get_driver(self) -> webdriver.Chrome:
        """
        Initialize and return a Chrome WebDriver instance.
        
        Returns:
            Configured Chrome WebDriver
        """
        if self.driver:
            return self.driver
            
        options = Options()
        
        if self.headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
        
        # Production-ready options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        # Get chromedriver path and ensure it's the executable, not a notice file
        driver_path = ChromeDriverManager().install()
        driver_path_obj = Path(driver_path)
        
        # If the path points to a directory or wrong file, find the actual chromedriver
        if driver_path_obj.is_dir() or 'NOTICES' in driver_path:
            # Look for chromedriver in the same directory
            parent_dir = driver_path_obj.parent if driver_path_obj.is_file() else driver_path_obj
            chromedriver = parent_dir / "chromedriver"
            if chromedriver.exists():
                driver_path = str(chromedriver)
                # Ensure it's executable
                chromedriver.chmod(0o755)
        
        service = Service(driver_path)
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(0)  # Force explicit waits only
        
        return self.driver
    
    def quit_driver(self) -> None:
        """Clean up driver resources."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"[WARNING] Error during driver cleanup: {e}")
            finally:
                self.driver = None
