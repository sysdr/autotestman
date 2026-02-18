"""
Demonstration test to verify configuration management.
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from framework.config_manager import ConfigManager
from framework.driver_factory import WebDriverFactory


class TestConfigurationDemo:
    """Test class demonstrating configuration-driven test execution."""
    
    @pytest.fixture(scope="function")
    def driver(self):
        """Fixture to create and cleanup WebDriver."""
        config = ConfigManager()
        config.print_current_config()
        
        driver = WebDriverFactory.create_driver()
        yield driver
        driver.quit()
    
    def test_login_with_configured_mode(self, driver):
        """
        Test login functionality using configuration-driven driver.
        
        This test will run in headless or UI mode based on config.ini
        without any code changes.
        """
        config = ConfigManager()
        
        # Navigate to base URL from config
        driver.get(config.get_base_url())
        
        # Wait for login elements
        wait = WebDriverWait(driver, 10)
        username_field = wait.until(
            EC.presence_of_element_located((By.ID, "user-name"))
        )
        
        # Perform login
        username_field.send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        # Verify login success
        inventory_container = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "inventory_container"))
        )
        
        assert inventory_container.is_displayed()
        print("✓ Login successful - Configuration-driven test passed!")
    
    def test_verify_headless_mode_setting(self):
        """Verify that headless mode can be read from configuration."""
        config = ConfigManager()
        headless = config.get_headless_mode()
        
        assert isinstance(headless, bool)
        print(f"✓ Headless mode setting verified: {headless}")
    
    def test_singleton_pattern(self):
        """Verify ConfigManager implements Singleton correctly."""
        config1 = ConfigManager()
        config2 = ConfigManager()
        
        assert config1 is config2, "ConfigManager should return the same instance"
        print("✓ Singleton pattern verified")


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "-s"])
