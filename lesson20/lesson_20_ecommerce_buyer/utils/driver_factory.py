"""
WebDriver Factory - Centralized driver initialization
"""
import os
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from typing import Literal


class DriverFactory:
    """Factory for creating WebDriver instances"""
    
    @staticmethod
    def create_driver(
        browser: Literal["chrome", "firefox"] = "chrome",
        headless: bool = False
    ) -> webdriver.Remote:
        """
        Create and configure WebDriver instance
        
        Args:
            browser: Browser type (chrome or firefox)
            headless: Run in headless mode
        
        Returns:
            Configured WebDriver instance
        """
        if browser == "chrome":
            return DriverFactory._create_chrome_driver(headless)
        elif browser == "firefox":
            return DriverFactory._create_firefox_driver(headless)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    @staticmethod
    def _create_chrome_driver(headless: bool) -> webdriver.Chrome:
        """Create Chrome driver with optimized options"""
        options = ChromeOptions()
        
        if headless:
            options.add_argument("--headless=new")
        
        # Performance optimizations
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        
        # Disable unnecessary features
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        
        # Handle browser alerts and authentication dialogs automatically
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.set_capability("unhandledPromptBehavior", "accept")
        
        # Try hardcoded path first (for local development), fallback to ChromeDriverManager
        chromedriver_path = "/home/systemdr03/.wdm/drivers/chromedriver/linux64/144.0.7559.133/chromedriver-linux64/chromedriver"
        
        if os.path.exists(chromedriver_path) and os.access(chromedriver_path, os.X_OK):
            # Use hardcoded path if it exists and is executable
            service = ChromeService(chromedriver_path)
        else:
            # Fallback to ChromeDriverManager for other users or if path doesn't exist
            service = ChromeService(ChromeDriverManager().install())
        
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(0)  # We use explicit waits
        
        return driver
    
    @staticmethod
    def _create_firefox_driver(headless: bool) -> webdriver.Firefox:
        """Create Firefox driver with optimized options"""
        options = FirefoxOptions()
        
        if headless:
            options.add_argument("--headless")
        
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        
        service = FirefoxService(GeckoDriverManager().install())
        
        driver = webdriver.Firefox(service=service, options=options)
        driver.implicitly_wait(0)
        
        return driver
