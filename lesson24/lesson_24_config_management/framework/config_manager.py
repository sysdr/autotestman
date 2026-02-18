"""
Configuration Manager - Singleton Pattern
Loads and provides access to configuration values from config.ini
"""

import os
from configparser import ConfigParser
from pathlib import Path
from typing import Optional


class ConfigManager:
    """
    Singleton class to manage application configuration.
    
    Design Pattern: Singleton
    Purpose: Load config.ini once and provide type-safe access to values.
    Thread-safe: No (use threading.Lock if needed in multi-threaded contexts)
    """
    
    _instance: Optional['ConfigManager'] = None
    _initialized: bool = False
    
    def __new__(cls):
        """
        Control object creation to ensure only one instance exists.
        
        This is called BEFORE __init__. We use it to implement Singleton.
        """
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """
        Initialize the configuration (only runs once due to _initialized flag).
        """
        if not ConfigManager._initialized:
            self._load_config()
            ConfigManager._initialized = True
    
    def _load_config(self):
        """Load configuration from config.ini file."""
        self.config = ConfigParser()
        
        # Find config.ini (works from any execution location)
        config_path = Path(__file__).parent.parent / "config" / "config.ini"
        
        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}\n"
                f"Please ensure config.ini exists in the config/ directory."
            )
        
        self.config.read(config_path)
        print(f"[ConfigManager] Loaded configuration from: {config_path}")
    
    def get_headless_mode(self) -> bool:
        """
        Get headless mode setting.
        
        Priority:
        1. Environment variable HEADLESS (if set)
        2. config.ini value
        
        Returns:
            bool: True for headless mode, False for UI mode
        """
        env_headless = os.getenv('HEADLESS')
        if env_headless is not None:
            return env_headless.lower() in ('true', '1', 'yes')
        
        return self.config.getboolean('BROWSER', 'headless', fallback=True)
    
    def get_browser_type(self) -> str:
        """Get browser type (chrome, firefox, edge)."""
        env_browser = os.getenv('BROWSER_TYPE')
        if env_browser is not None:
            return env_browser.lower()
        
        return self.config.get('BROWSER', 'browser_type', fallback='chrome')
    
    def get_implicit_wait(self) -> int:
        """Get implicit wait timeout in seconds."""
        return self.config.getint('BROWSER', 'implicit_wait', fallback=10)
    
    def get_page_load_timeout(self) -> int:
        """Get page load timeout in seconds."""
        return self.config.getint('BROWSER', 'page_load_timeout', fallback=30)
    
    def get_window_size(self) -> tuple[int, int]:
        """Get window size for headless mode."""
        width = self.config.getint('BROWSER', 'window_width', fallback=1920)
        height = self.config.getint('BROWSER', 'window_height', fallback=1080)
        return (width, height)
    
    def get_base_url(self) -> str:
        """Get base URL for testing."""
        env_url = os.getenv('BASE_URL')
        if env_url is not None:
            return env_url
        
        return self.config.get('ENVIRONMENT', 'base_url', fallback='https://www.saucedemo.com')
    
    def get_test_timeout(self) -> int:
        """Get test execution timeout in seconds."""
        return self.config.getint('ENVIRONMENT', 'test_timeout', fallback=60)
    
    def get_log_level(self) -> str:
        """Get logging level."""
        return self.config.get('LOGGING', 'log_level', fallback='INFO')
    
    def print_current_config(self):
        """Print all current configuration values (useful for debugging)."""
        print("\n" + "="*60)
        print("CURRENT CONFIGURATION")
        print("="*60)
        print(f"Headless Mode: {self.get_headless_mode()}")
        print(f"Browser Type: {self.get_browser_type()}")
        print(f"Implicit Wait: {self.get_implicit_wait()}s")
        print(f"Page Load Timeout: {self.get_page_load_timeout()}s")
        print(f"Window Size: {self.get_window_size()}")
        print(f"Base URL: {self.get_base_url()}")
        print(f"Test Timeout: {self.get_test_timeout()}s")
        print(f"Log Level: {self.get_log_level()}")
        print("="*60 + "\n")


# Verify singleton behavior
if __name__ == "__main__":
    print("Testing ConfigManager Singleton Pattern...")
    
    config1 = ConfigManager()
    config2 = ConfigManager()
    
    print(f"config1 instance id: {id(config1)}")
    print(f"config2 instance id: {id(config2)}")
    print(f"Same instance? {config1 is config2}")
    
    config1.print_current_config()
