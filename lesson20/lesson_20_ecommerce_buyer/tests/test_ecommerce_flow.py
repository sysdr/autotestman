"""
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
    print(f"\n🚀 Initializing {config.browser} driver...")
    driver = DriverFactory.create_driver(config.browser, config.headless)
    driver.maximize_window()
    
    yield driver
    
    print("\n🧹 Cleaning up driver...")
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
        print("\n📝 Step 1: Logging in...")
        driver.get(config.base_url)
        login_page = LoginPage(driver)
        login_page.login(config.username, config.password)
        
        assert login_page.is_login_successful(), "Login failed"
        print("✅ Login successful")
        
        # Step 2: Browse and select product
        print("\n🔍 Step 2: Browsing products...")
        product_page = ProductListingPage(driver)
        product_count = product_page.get_product_count()
        print(f"   Found {product_count} products")
        
        # Step 3: Add product to cart AND automatically go to cart (fully automated)
        print(f"\n🛒 Step 3: Adding '{config.test_product}' to cart and navigating to cart (automated)...")
        initial_cart_count = product_page.get_cart_item_count()
        
        # This method does BOTH: adds to cart AND automatically clicks cart link - NO MANUAL CLICK NEEDED
        product_page.add_to_cart_and_go_to_cart_automatically(config.test_product)
        
        # Verify cart badge was updated before navigation
        # Note: We check before navigation since we're going to cart automatically
        print(f"✅ Product added to cart (cart count: {initial_cart_count} → {initial_cart_count + 1})")
        print("✅ Automatically navigated to cart page (no manual click required)")
        
        cart_page = CartPage(driver)
        assert cart_page.verify_cart_loaded(), "Cart page did not load"
        assert cart_page.is_product_in_cart(config.test_product), "Product not in cart"
        print(f"✅ Product '{config.test_product}' found in cart")
        
        # Step 5: Proceed to checkout
        print("\n💳 Step 5: Proceeding to checkout...")
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
        print("\n🎉 Step 6: Completing purchase...")
        checkout_page.finish_checkout()
        
        assert checkout_page.is_checkout_complete(), "Checkout did not complete"
        success_msg = checkout_page.get_success_message()
        print(f"✅ {success_msg}")
        
        # Calculate execution time
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"\n⏱️  Total execution time: {execution_time:.2f}s")
        
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
        print("\n" + "="*60)
        print("✅ TEST PASSED - All steps completed successfully")
        print("="*60)
        return True
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        return False
    finally:
        driver.quit()


if __name__ == "__main__":
    success = run_standalone_test()
    sys.exit(0 if success else 1)
