"""
WebDriver Factory - Factory Pattern
Creates properly configured WebDriver instances based on configuration.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

from framework.config_manager import ConfigManager


class WebDriverFactory:
    """
    Factory class to create WebDriver instances.
    
    Design Pattern: Factory
    Purpose: Encapsulate driver creation logic and apply configuration.
    """
    
    @staticmethod
    def create_driver() -> webdriver.Chrome | webdriver.Firefox:
        """
        Create a WebDriver instance based on configuration.
        
        Returns:
            WebDriver instance (Chrome or Firefox)
        
        Raises:
            ValueError: If unsupported browser type is specified
        """
        config = ConfigManager()
        browser_type = config.get_browser_type()
        
        if browser_type == 'chrome':
            return WebDriverFactory._create_chrome_driver(config)
        elif browser_type == 'firefox':
            return WebDriverFactory._create_firefox_driver(config)
        else:
            raise ValueError(f"Unsupported browser type: {browser_type}")
    
    @staticmethod
    def _create_chrome_driver(config: ConfigManager) -> webdriver.Chrome:
        """Create Chrome WebDriver with proper configuration."""
        options = ChromeOptions()
        
        # Headless mode configuration
        if config.get_headless_mode():
            options.add_argument("--headless=new")  # New headless mode (Chrome 109+)
            options.add_argument("--no-sandbox")  # Required for CI/CD
            options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
            options.add_argument("--disable-gpu")  # Applicable to Windows
            
            # Set window size for headless
            width, height = config.get_window_size()
            options.add_argument(f"--window-size={width},{height}")
        
        # Additional stability options
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Create driver
        driver = webdriver.Chrome(options=options)
        
        # Apply timeouts
        driver.implicitly_wait(config.get_implicit_wait())
        driver.set_page_load_timeout(config.get_page_load_timeout())
        
        # Maximize window if not headless
        if not config.get_headless_mode():
            driver.maximize_window()
        
        print(f"[WebDriverFactory] Created Chrome driver (headless={config.get_headless_mode()})")
        return driver
    
    @staticmethod
    def _create_firefox_driver(config: ConfigManager) -> webdriver.Firefox:
        """Create Firefox WebDriver with proper configuration."""
        options = FirefoxOptions()
        
        # Headless mode configuration
        if config.get_headless_mode():
            options.add_argument("--headless")
            
            # Set window size for headless
            width, height = config.get_window_size()
            options.add_argument(f"--width={width}")
            options.add_argument(f"--height={height}")
        
        # Create driver
        driver = webdriver.Firefox(options=options)
        
        # Apply timeouts
        driver.implicitly_wait(config.get_implicit_wait())
        driver.set_page_load_timeout(config.get_page_load_timeout())
        
        # Maximize window if not headless
        if not config.get_headless_mode():
            driver.maximize_window()
        
        print(f"[WebDriverFactory] Created Firefox driver (headless={config.get_headless_mode()})")
        return driver


# Test the factory
if __name__ == "__main__":
    print("Testing WebDriverFactory...")
    
    driver = WebDriverFactory.create_driver()
    print(f"Driver created: {type(driver).__name__}")
    
    driver.get("https://www.saucedemo.com")
    print(f"Page title: {driver.title}")
    
    driver.quit()
    print("Driver closed successfully")
