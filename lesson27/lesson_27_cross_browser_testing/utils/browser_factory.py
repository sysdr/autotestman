"""
Browser Factory Module
======================
Centralized browser instance creation using the Factory Pattern.
Handles automatic driver management via webdriver-manager.
"""

import os
from typing import Dict, Any
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

try:
    from webdriver_manager.chrome import ChromeDriverManager
    WDM_AVAILABLE = True
except ImportError:
    WDM_AVAILABLE = False


def _resolve_driver_path(wdm_path: str, binary_name: str) -> str:
    """
    Resolve WDM path to the actual driver binary.
    Recent ChromeDriver (115+) downloads include THIRD_PARTY_NOTICES.chromedriver;
    WDM can return the wrong file, so we ensure we use the executable binary.
    """
    driver_dir = os.path.dirname(wdm_path)
    binary_path = os.path.join(driver_dir, binary_name)
    if os.path.isfile(binary_path) and os.access(binary_path, os.X_OK):
        return binary_path
    return wdm_path


class BrowserFactory:
    """Factory class for creating Chrome WebDriver instances."""
    
    SUPPORTED_BROWSERS = ["chrome"]
    
    @staticmethod
    def create_driver(browser_name: str, headless: bool = False,
                     options: Dict[str, Any] = None) -> webdriver.Remote:
        """
        Create a Chrome WebDriver instance.

        Args:
            browser_name: Must be "chrome"
            headless: Whether to run in headless mode
            options: Additional Chrome options

        Returns:
            WebDriver instance

        Raises:
            ValueError: If browser is not supported
            ImportError: If webdriver-manager is not installed
        """
        if not WDM_AVAILABLE:
            raise ImportError(
                "webdriver-manager is required. Install it with: "
                "pip install webdriver-manager"
            )
        browser_name = browser_name.lower()
        if browser_name not in BrowserFactory.SUPPORTED_BROWSERS:
            raise ValueError(
                f"Unsupported browser: {browser_name}. "
                f"Supported: {BrowserFactory.SUPPORTED_BROWSERS}"
            )
        options = options or {}
        return BrowserFactory._create_chrome(headless, options)

    @staticmethod
    def _create_chrome(headless: bool, custom_options: Dict[str, Any]) -> webdriver.Chrome:
        """Create Chrome WebDriver instance."""
        chrome_options = ChromeOptions()
        
        if headless:
            chrome_options.add_argument("--headless=new")
        
        # Standard options for stability
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Apply custom options
        for key, value in custom_options.items():
            chrome_options.add_argument(f"--{key}={value}")
        
        wdm_path = ChromeDriverManager().install()
        driver_path = _resolve_driver_path(wdm_path, "chromedriver")
        service = ChromeService(driver_path)
        return webdriver.Chrome(service=service, options=chrome_options)


class BrowserConfig:
    """Configuration for browser testing."""
    
    DEFAULT_TIMEOUT = 10
    DEFAULT_IMPLICIT_WAIT = 5
    DEFAULT_PAGE_LOAD_TIMEOUT = 30
    
    @staticmethod
    def configure_driver(driver: webdriver.Remote) -> None:
        """Apply standard timeouts and configurations to a driver."""
        driver.implicitly_wait(BrowserConfig.DEFAULT_IMPLICIT_WAIT)
        driver.set_page_load_timeout(BrowserConfig.DEFAULT_PAGE_LOAD_TIMEOUT)
