"""
CartPage - Handles shopping cart operations
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from typing import List
import time


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
        """Click checkout button automatically - NO MANUAL CLICK REQUIRED"""
        # Try multiple selectors to ensure we find the checkout button
        checkout_button = None
        selectors = [
            self.CHECKOUT_BUTTON,  # Primary: ID selector
            (By.CSS_SELECTOR, "button#checkout"),  # Alternative: CSS selector
            (By.CSS_SELECTOR, "#checkout"),  # Alternative: CSS ID
            (By.XPATH, "//button[@id='checkout']"),  # Alternative: XPath
            (By.XPATH, "//*[@id='checkout']"),  # Alternative: XPath any element
        ]
        
        # Find the checkout button using any available selector
        for selector in selectors:
            try:
                checkout_button = self.wait.until(EC.element_to_be_clickable(selector))
                break
            except:
                continue
        
        if checkout_button is None:
            raise Exception("Checkout button not found - cannot proceed to checkout automatically")
        
        # Wait a moment for any animations/overlays to settle (handles timing issues)
        print("   ⏳ Waiting for page to stabilize before clicking checkout...")
        time.sleep(2)  # Small wait to handle timing/animation issues
        
        # FORCE CLICK - This MUST happen automatically, no manual click needed
        # Use JavaScript click to handle overlay/animation issues
        print("   🔄 Automatically clicking checkout button using JavaScript (no manual click required)...")
        try:
            # Try JavaScript click first (handles overlay/animation issues)
            self.driver.execute_script("arguments[0].click();", checkout_button)
            print("   ✅ JavaScript click executed successfully")
        except Exception as js_error:
            # Fallback to regular click if JavaScript click fails
            print(f"   ⚠️  JavaScript click failed, trying regular click: {js_error}")
            checkout_button.click()  # Fallback to regular click
        
        # Small wait to ensure click registered
        time.sleep(0.3)
        
        # Handle any alerts that might appear
        self.handle_alert(accept=True)
        
        # Wait for checkout information page to load
        print("   ⏳ Waiting for checkout page to load...")
        # Try multiple URL patterns and element checks
        try:
            self.wait.until(
                EC.any_of(
                    EC.url_contains("/checkout-step-one"),
                    EC.url_contains("checkout"),
                    EC.presence_of_element_located((By.ID, "first-name")),
                    EC.presence_of_element_located((By.ID, "last-name"))
                )
            )
            print("   ✅ Checkout page loaded successfully")
        except:
            # Fallback: just wait a bit and check URL
            time.sleep(1)
            if "checkout" in self.driver.current_url.lower():
                print("   ✅ Checkout page loaded successfully")
            else:
                raise Exception("Checkout page did not load after clicking checkout button")
    
    def continue_shopping(self) -> None:
        """Return to product listing"""
        self.wait_and_click(self.CONTINUE_SHOPPING)
    
    def verify_cart_loaded(self) -> bool:
        """Verify cart page loaded successfully"""
        # Check for cart page elements instead of URL (more reliable)
        try:
            # Wait for either cart items or checkout button to be present
            self.wait.until(EC.any_of(
                EC.presence_of_element_located(self.CART_ITEMS),
                EC.presence_of_element_located(self.CHECKOUT_BUTTON)
            ))
            return True
        except:
            # Fallback to URL check
            return self.wait_for_url_contains("cart")
