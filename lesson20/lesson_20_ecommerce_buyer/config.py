"""
Configuration for E-Commerce Buyer Test Suite
"""
from pathlib import Path
from dataclasses import dataclass


# Project paths
PROJECT_ROOT = Path(__file__).parent
REPORTS_DIR = PROJECT_ROOT / "reports"


@dataclass
class TestConfig:
    """Test execution configuration"""
    base_url: str = "https://www.saucedemo.com"  # Demo e-commerce site
    implicit_wait: int = 0  # We use explicit waits
    explicit_wait: int = 10
    browser: str = "chrome"
    headless: bool = False
    
    # Test data
    username: str = "standard_user"
    password: str = "secret_sauce"
    test_product: str = "Sauce Labs Backpack"


# Global config instance
config = TestConfig()
