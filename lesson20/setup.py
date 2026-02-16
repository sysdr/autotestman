#!/usr/bin/env python3
"""
Lesson 20: The E-Commerce Buyer - Complete Workspace Setup
UQAP - Unified Quality Assurance Platform

This script generates a complete, production-ready e-commerce test automation project.
Run: python setup_lesson.py
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
import subprocess


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_status(message: str, status: str = "INFO"):
    """Print formatted status message"""
    color = {
        "INFO": Colors.BLUE,
        "SUCCESS": Colors.GREEN,
        "WARNING": Colors.YELLOW,
        "ERROR": Colors.RED
    }.get(status, Colors.RESET)
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{color}[{timestamp}] [{status}]{Colors.RESET} {message}")


def create_directory_structure(base_path: Path) -> dict[str, Path]:
    """Create project directory structure"""
    print_status("Creating directory structure...", "INFO")
    
    dirs = {
        'root': base_path,
        'pages': base_path / 'pages',
        'tests': base_path / 'tests',
        'utils': base_path / 'utils',
        'reports': base_path / 'reports'
    }
    
    for name, path in dirs.items():
        path.mkdir(parents=True, exist_ok=True)
        print_status(f"Created: {path}", "SUCCESS")
    
    return dirs


def generate_config_file(root_path: Path):
    """Generate config.py with project configuration"""
    content = '''"""
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
'''
    
    filepath = root_path / "config.py"
    filepath.write_text(content)
    print_status(f"Generated: {filepath}", "SUCCESS")


def generate_driver_factory(utils_path: Path):
    """Generate utils/driver_factory.py"""
    content = '''"""
WebDriver Factory - Centralized driver initialization
"""
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
'''
    
    filepath = utils_path / "driver_factory.py"
    filepath.write_text(content)
    print_status(f"Generated: {filepath}", "SUCCESS")


def generate_base_page(pages_path: Path):
    """Generate pages/base_page.py"""
    content = '''"""
BasePage - Foundation for all Page Objects
Provides reusable wait mechanisms and common operations
"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Tuple
import time


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.timeout = timeout
    
    def wait_and_find(self, locator: Tuple[str, str]) -> WebElement:
        """
        Wait for element to be present in DOM
        
        Args:
            locator: Tuple of (By.X, "selector")
        
        Returns:
            WebElement when found
        
        Raises:
            TimeoutException: If element not found within timeout
        """
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(
                f"Element not found within {self.timeout}s: {locator}"
            )
    
    def wait_and_click(self, locator: Tuple[str, str]) -> WebElement:
        """
        Wait for element to be clickable, then click it
        
        This checks:
        - Element is present in DOM
        - Element is visible
        - Element is enabled
        - Element is not obscured
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            return element
        except TimeoutException:
            raise TimeoutException(
                f"Element not clickable within {self.timeout}s: {locator}"
            )
    
    def wait_and_send_keys(
        self, 
        locator: Tuple[str, str], 
        text: str,
        clear_first: bool = True
    ) -> WebElement:
        """
        Wait for element to be present, optionally clear it, then send keys
        """
        element = self.wait_and_find(locator)
        
        if clear_first:
            element.clear()
        
        element.send_keys(text)
        return element
    
    def wait_for_url_contains(self, url_fragment: str) -> bool:
        """Wait for URL to contain specific fragment"""
        try:
            self.wait.until(EC.url_contains(url_fragment))
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_text(
        self, 
        locator: Tuple[str, str], 
        expected_text: str
    ) -> bool:
        """Wait for element to contain specific text"""
        try:
            self.wait.until(
                EC.text_to_be_present_in_element(locator, expected_text)
            )
            return True
        except TimeoutException:
            return False
    
    def get_element_text(self, locator: Tuple[str, str]) -> str:
        """Get text content of element"""
        element = self.wait_and_find(locator)
        return element.text
    
    def is_element_visible(self, locator: Tuple[str, str]) -> bool:
        """Check if element is visible without waiting"""
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except:
            return False
'''
    
    filepath = pages_path / "base_page.py"
    filepath.write_text(content)
    print_status(f"Generated: {filepath}", "SUCCESS")


def generate_login_page(pages_path: Path):
    """Generate pages/login_page.py"""
    content = '''"""
LoginPage - Handles authentication
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for login functionality"""
    
    # Locators
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    def login(self, username: str, password: str) -> None:
        """
        Perform login action
        
        Args:
            username: User credential
            password: User credential
        """
        self.wait_and_send_keys(self.USERNAME_INPUT, username)
        self.wait_and_send_keys(self.PASSWORD_INPUT, password)
        self.wait_and_click(self.LOGIN_BUTTON)
    
    def is_login_successful(self) -> bool:
        """Check if login was successful by checking URL"""
        return self.wait_for_url_contains("/inventory.html")
    
    def get_error_message(self) -> str:
        """Get error message if login fails"""
        return self.get_element_text(self.ERROR_MESSAGE)
'''
    
    filepath = pages_path / "login_page.py"
    filepath.write_text(content)
    print_status(f"Generated: {filepath}", "SUCCESS")


def generate_product_listing_page(pages_path: Path):
    """Generate pages/product_listing_page.py"""
    content = '''"""
ProductListingPage - Handles product browsing and search
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage
from typing import List


class ProductListingPage(BasePage):
    """Page Object for product listing/inventory"""
    
    # Locators
    PRODUCT_CARDS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_TITLE = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    
    def get_product_count(self) -> int:
        """Get number of products displayed"""
        products = self.wait.until(
            lambda d: d.find_elements(*self.PRODUCT_CARDS)
        )
        return len(products)
    
    def get_product_by_name(self, product_name: str) -> WebElement:
        """
        Find product card by name
        
        Args:
            product_name: Exact product name to search for
        
        Returns:
            WebElement of the product card
        
        Raises:
            ValueError: If product not found
        """
        products = self.driver.find_elements(*self.PRODUCT_CARDS)
        
        for product in products:
            title_element = product.find_element(By.CLASS_NAME, "inventory_item_name")
            if title_element.text == product_name:
                return product
        
        raise ValueError(f"Product not found: {product_name}")
    
    def add_product_to_cart(self, product_name: str) -> None:
        """
        Add specific product to cart by name
        
        Args:
            product_name: Name of product to add
        """
        product_card = self.get_product_by_name(product_name)
        add_button = product_card.find_element(*self.ADD_TO_CART_BUTTON)
        add_button.click()
    
    def get_cart_item_count(self) -> int:
        """
        Get number of items in cart from badge
        
        Returns:
            Item count, or 0 if badge not visible
        """
        if self.is_element_visible(self.CART_BADGE):
            badge_text = self.get_element_text(self.CART_BADGE)
            return int(badge_text)
        return 0
    
    def click_cart_link(self) -> None:
        """Navigate to cart page"""
        self.wait_and_click(self.CART_LINK)
    
    def get_product_price(self, product_name: str) -> str:
        """Get price of specific product"""
        product_card = self.get_product_by_name(product_name)
        price_element = product_card.find_element(*self.PRODUCT_PRICE)
        return price_element.text
'''
    
    filepath = pages_path / "product_listing_page.py"
    filepath.write_text(content)
    print_status(f"Generated: {filepath}", "SUCCESS")


def generate_cart_page(pages_path: Path):
    """Generate pages/cart_page.py"""
    content = '''"""
CartPage - Handles shopping cart operations
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from typing import List


class CartPage(BasePage):
    """Page Object for shopping cart"""
    
    # Locators
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button[id^='remove']")
    
    def get_cart_item_count(self) -> int:
        """Get number of items in cart"""
        items = self.driver.find_elements(*self.CART_ITEMS)
        return len(items)
    
    def get_cart_item_names(self) -> List[str]:
        """Get names of all items in cart"""
        items = self.driver.find_elements(*self.ITEM_NAME)
        return [item.text for item in items]
    
    def is_product_in_cart(self, product_name: str) -> bool:
        """Check if specific product is in cart"""
        return product_name in self.get_cart_item_names()
    
    def proceed_to_checkout(self) -> None:
        """Click checkout button"""
        self.wait_and_click(self.CHECKOUT_BUTTON)
    
    def continue_shopping(self) -> None:
        """Return to product listing"""
        self.wait_and_click(self.CONTINUE_SHOPPING)
    
    def verify_cart_loaded(self) -> bool:
        """Verify cart page loaded successfully"""
        return self.wait_for_url_contains("/cart.html")
'''
    
    filepath = pages_path / "cart_page.py"
    filepath.write_text(content)
    print_status(f"Generated: {filepath}", "SUCCESS")


def generate_checkout_page(pages_path: Path):
    """Generate pages/checkout_page.py"""
    content = '''"""
CheckoutPage - Handles checkout process
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from dataclasses import dataclass


@dataclass
class CheckoutInfo:
    """Customer checkout information"""
    first_name: str
    last_name: str
    postal_code: str


class CheckoutPage(BasePage):
    """Page Object for checkout flow"""
    
    # Step 1: Information
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    
    # Step 2: Overview
    FINISH_BUTTON = (By.ID, "finish")
    TOTAL_PRICE = (By.CLASS_NAME, "summary_total_label")
    
    # Step 3: Complete
    SUCCESS_MESSAGE = (By.CLASS_NAME, "complete-header")
    
    def fill_checkout_information(self, info: CheckoutInfo) -> None:
        """
        Fill checkout form
        
        Args:
            info: CheckoutInfo dataclass with customer details
        """
        self.wait_and_send_keys(self.FIRST_NAME_INPUT, info.first_name)
        self.wait_and_send_keys(self.LAST_NAME_INPUT, info.last_name)
        self.wait_and_send_keys(self.POSTAL_CODE_INPUT, info.postal_code)
        self.wait_and_click(self.CONTINUE_BUTTON)
    
    def finish_checkout(self) -> None:
        """Complete the purchase"""
        self.wait_and_click(self.FINISH_BUTTON)
    
    def get_success_message(self) -> str:
        """Get order completion message"""
        return self.get_element_text(self.SUCCESS_MESSAGE)
    
    def is_checkout_complete(self) -> bool:
        """Verify checkout completed successfully"""
        return self.wait_for_url_contains("/checkout-complete.html")
'''
    
    filepath = pages_path / "checkout_page.py"
    filepath.write_text(content)
    print_status(f"Generated: {filepath}", "SUCCESS")


def generate_init_files(dirs: dict):
    """Generate __init__.py files for packages"""
    for name in ['pages', 'tests', 'utils']:
        init_file = dirs[name] / "__init__.py"
        init_file.write_text('"""Package initialization"""\n')
        print_status(f"Generated: {init_file}", "SUCCESS")


def generate_test_file(tests_path: Path):
    """Generate tests/test_ecommerce_flow.py"""
    content = '''"""
E-Commerce Buyer Flow Test
Tests the complete purchase journey from login to checkout
"""
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
import time
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import config
from utils.driver_factory import DriverFactory
from pages.login_page import LoginPage
from pages.product_listing_page import ProductListingPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage, CheckoutInfo


@pytest.fixture(scope="function")
def driver():
    """Create and teardown WebDriver for each test"""
    print(f"\\n🚀 Initializing {config.browser} driver...")
    driver = DriverFactory.create_driver(config.browser, config.headless)
    driver.maximize_window()
    
    yield driver
    
    print("\\n🧹 Cleaning up driver...")
    driver.quit()


class TestECommerceBuyerFlow:
    """Test suite for complete purchase flow"""
    
    def test_complete_purchase_flow(self, driver: WebDriver):
        """
        Test Case: Complete E-Commerce Purchase Flow
        
        Steps:
        1. Login to the store
        2. Browse products
        3. Add product to cart
        4. Verify cart
        5. Proceed to checkout
        6. Complete purchase
        
        Expected Result: Order placed successfully
        """
        start_time = time.time()
        
        # Step 1: Login
        print("\\n📝 Step 1: Logging in...")
        driver.get(config.base_url)
        login_page = LoginPage(driver)
        login_page.login(config.username, config.password)
        
        assert login_page.is_login_successful(), "Login failed"
        print("✅ Login successful")
        
        # Step 2: Browse and select product
        print("\\n🔍 Step 2: Browsing products...")
        product_page = ProductListingPage(driver)
        product_count = product_page.get_product_count()
        print(f"   Found {product_count} products")
        
        # Step 3: Add product to cart
        print(f"\\n🛒 Step 3: Adding '{config.test_product}' to cart...")
        initial_cart_count = product_page.get_cart_item_count()
        product_page.add_product_to_cart(config.test_product)
        
        # Verify cart badge updated
        final_cart_count = product_page.get_cart_item_count()
        assert final_cart_count == initial_cart_count + 1, "Cart count did not update"
        print(f"✅ Cart updated: {initial_cart_count} → {final_cart_count}")
        
        # Step 4: Go to cart and verify
        print("\\n🛍️ Step 4: Verifying cart contents...")
        product_page.click_cart_link()
        
        cart_page = CartPage(driver)
        assert cart_page.verify_cart_loaded(), "Cart page did not load"
        assert cart_page.is_product_in_cart(config.test_product), "Product not in cart"
        print(f"✅ Product '{config.test_product}' found in cart")
        
        # Step 5: Proceed to checkout
        print("\\n💳 Step 5: Proceeding to checkout...")
        cart_page.proceed_to_checkout()
        
        checkout_page = CheckoutPage(driver)
        
        # Fill checkout information
        checkout_info = CheckoutInfo(
            first_name="John",
            last_name="Doe",
            postal_code="12345"
        )
        checkout_page.fill_checkout_information(checkout_info)
        print("✅ Checkout information filled")
        
        # Step 6: Complete purchase
        print("\\n🎉 Step 6: Completing purchase...")
        checkout_page.finish_checkout()
        
        assert checkout_page.is_checkout_complete(), "Checkout did not complete"
        success_msg = checkout_page.get_success_message()
        print(f"✅ {success_msg}")
        
        # Calculate execution time
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"\\n⏱️  Total execution time: {execution_time:.2f}s")
        
        # Production readiness check
        assert execution_time < 20, f"Test too slow: {execution_time:.2f}s > 20s"
        print("✅ Performance within acceptable range")


def run_standalone_test():
    """Run test without pytest for demonstration"""
    print("="*60)
    print("E-COMMERCE BUYER FLOW - STANDALONE EXECUTION")
    print("="*60)
    
    driver = DriverFactory.create_driver(config.browser, config.headless)
    driver.maximize_window()
    
    try:
        test = TestECommerceBuyerFlow()
        test.test_complete_purchase_flow(driver)
        print("\\n" + "="*60)
        print("✅ TEST PASSED - All steps completed successfully")
        print("="*60)
        return True
    except Exception as e:
        print(f"\\n❌ TEST FAILED: {str(e)}")
        return False
    finally:
        driver.quit()


if __name__ == "__main__":
    success = run_standalone_test()
    sys.exit(0 if success else 1)
'''
    
    filepath = tests_path / "test_ecommerce_flow.py"
    filepath.write_text(content)
    print_status(f"Generated: {filepath}", "SUCCESS")


def generate_requirements_file(root_path: Path):
    """Generate requirements.txt"""
    content = '''# E-Commerce Buyer Test Suite Dependencies
selenium>=4.15.0
webdriver-manager>=4.0.1
pytest>=7.4.0
pytest-html>=4.1.1
'''
    
    filepath = root_path / "requirements.txt"
    filepath.write_text(content)
    print_status(f"Generated: {filepath}", "SUCCESS")


def generate_readme(root_path: Path):
    """Generate README.md"""
    content = '''# Lesson 20: The E-Commerce Buyer

## Project Structure
```
lesson_20_ecommerce_buyer/
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── pages/                    # Page Object Model
│   ├── base_page.py         # Reusable wait mechanisms
│   ├── login_page.py        # Login functionality
│   ├── product_listing_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/                    # Test cases
│   └── test_ecommerce_flow.py
└── utils/                    # Utilities
    └── driver_factory.py    # WebDriver initialization
```

## Setup
```bash
pip install -r requirements.txt
```

## Run Tests

### With pytest (recommended):
```bash
pytest tests/test_ecommerce_flow.py -v -s
```

### Standalone:
```bash
python tests/test_ecommerce_flow.py
```

## What You'll Learn
- ✅ Explicit waits vs implicit waits
- ✅ Page Object Model pattern
- ✅ Custom expected conditions
- ✅ Production-ready test architecture
- ✅ Zero hard sleeps policy

## Success Metrics
- Test Stability: > 99%
- Execution Time: < 20s
- Zero `time.sleep()` usage
'''
    
    filepath = root_path / "README.md"
    filepath.write_text(content)
    print_status(f"Generated: {filepath}", "SUCCESS")


def generate_html_report(root_path: Path):
    """Generate an HTML visualization of the test structure"""
    content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-Commerce Buyer - Project Structure</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        h1 {
            color: #2d3748;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .subtitle {
            color: #718096;
            margin-bottom: 40px;
            font-size: 1.2em;
        }
        .architecture {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }
        .layer {
            background: #f7fafc;
            border-radius: 12px;
            padding: 24px;
            border-left: 4px solid #667eea;
        }
        .layer h2 {
            color: #2d3748;
            margin-bottom: 16px;
            font-size: 1.4em;
        }
        .layer ul {
            list-style: none;
        }
        .layer li {
            padding: 8px 12px;
            margin: 6px 0;
            background: white;
            border-radius: 6px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            color: #4a5568;
        }
        .metrics {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 20px;
            margin-top: 40px;
        }
        .metric {
            flex: 1;
            min-width: 200px;
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #6ee7b7 0%, #3d93f5 100%);
            border-radius: 12px;
            color: white;
        }
        .metric-value {
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .metric-label {
            font-size: 1.1em;
            opacity: 0.9;
        }
        .status {
            display: inline-block;
            padding: 6px 12px;
            background: #48bb78;
            color: white;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛒 E-Commerce Buyer Test Suite</h1>
        <p class="subtitle">Production-Ready Web Automation with Selenium & Page Object Model</p>
        <span class="status">✅ SETUP COMPLETE</span>
        
        <div class="architecture">
            <div class="layer">
                <h2>📄 Pages Layer</h2>
                <ul>
                    <li>base_page.py</li>
                    <li>login_page.py</li>
                    <li>product_listing_page.py</li>
                    <li>cart_page.py</li>
                    <li>checkout_page.py</li>
                </ul>
            </div>
            
            <div class="layer">
                <h2>🧪 Tests Layer</h2>
                <ul>
                    <li>test_ecommerce_flow.py</li>
                    <li>└─ test_complete_purchase_flow()</li>
                </ul>
            </div>
            
            <div class="layer">
                <h2>🔧 Utils Layer</h2>
                <ul>
                    <li>driver_factory.py</li>
                    <li>config.py</li>
                </ul>
            </div>
        </div>
        
        <div class="metrics">
            <div class="metric">
                <div class="metric-value">0</div>
                <div class="metric-label">Hard Sleeps</div>
            </div>
            <div class="metric">
                <div class="metric-value">&lt;20s</div>
                <div class="metric-label">Execution Time</div>
            </div>
            <div class="metric">
                <div class="metric-value">99%+</div>
                <div class="metric-label">Test Stability</div>
            </div>
        </div>
    </div>
</body>
</html>
'''
    
    filepath = root_path / "project_structure.html"
    filepath.write_text(content)
    print_status(f"Generated: {filepath}", "SUCCESS")
    print_status(f"View at: file://{filepath.absolute()}", "INFO")


def main():
    """Main setup function"""
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}  LESSON 20: THE E-COMMERCE BUYER - WORKSPACE SETUP{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")
    
    # Create project structure
    project_name = "lesson_20_ecommerce_buyer"
    base_path = Path.cwd() / project_name
    
    if base_path.exists():
        print_status(f"Directory {project_name} already exists. Recreating...", "WARNING")
        import shutil
        shutil.rmtree(base_path)
    
    dirs = create_directory_structure(base_path)
    
    # Generate all files
    print_status("\nGenerating project files...", "INFO")
    generate_config_file(dirs['root'])
    generate_driver_factory(dirs['utils'])
    generate_base_page(dirs['pages'])
    generate_login_page(dirs['pages'])
    generate_product_listing_page(dirs['pages'])
    generate_cart_page(dirs['pages'])
    generate_checkout_page(dirs['pages'])
    generate_init_files(dirs)
    generate_test_file(dirs['tests'])
    generate_requirements_file(dirs['root'])
    generate_readme(dirs['root'])
    generate_html_report(dirs['root'])
    
    print(f"\n{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD}✅ WORKSPACE SETUP COMPLETE!{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*60}{Colors.RESET}\n")
    
    print(f"{Colors.BLUE}Next Steps:{Colors.RESET}")
    print(f"1. cd {project_name}")
    print(f"2. pip install -r requirements.txt")
    print(f"3. python tests/test_ecommerce_flow.py")
    print(f"\n{Colors.YELLOW}Or with pytest:{Colors.RESET}")
    print(f"   pytest tests/test_ecommerce_flow.py -v -s\n")
    
    # Open visualization
    html_file = base_path / "project_structure.html"
    print_status(f"Opening project visualization...", "INFO")
    try:
        import webbrowser
        webbrowser.open(f"file://{html_file.absolute()}")
    except:
        print_status(f"Could not open browser. View manually: {html_file}", "WARNING")


if __name__ == "__main__":
    main()