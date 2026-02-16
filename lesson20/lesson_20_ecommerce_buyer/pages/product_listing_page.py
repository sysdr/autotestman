"""
ProductListingPage - Handles product browsing and search
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
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
        # Wait a moment for cart to update
        import time
        time.sleep(0.5)
    
    def add_to_cart_and_go_to_cart_automatically(self, product_name: str) -> None:
        """
        Add product to cart AND automatically navigate to cart page in one step
        NO MANUAL CLICKS REQUIRED - completely automated
        
        Args:
            product_name: Name of product to add
        """
        # Step 1: Add product to cart (automated)
        self.add_product_to_cart(product_name)
        # Step 2: Automatically click cart link and navigate (automated - no manual click)
        self.click_cart_link()
    
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
        """Navigate to cart page automatically - NO MANUAL CLICK REQUIRED"""
        from selenium.webdriver.common.by import By
        import time
        
        # Try multiple selectors to ensure we find the cart link
        cart_link = None
        selectors = [
            self.CART_LINK,  # Primary: class name
            (By.CSS_SELECTOR, "a.shopping_cart_link"),  # Alternative: CSS selector
            (By.CSS_SELECTOR, ".shopping_cart_link"),  # Alternative: CSS class
            (By.XPATH, "//a[@class='shopping_cart_link']"),  # Alternative: XPath
        ]
        
        # Find the cart link using any available selector
        for selector in selectors:
            try:
                cart_link = self.wait.until(EC.element_to_be_clickable(selector))
                break
            except:
                continue
        
        if cart_link is None:
            raise Exception("Cart link not found - cannot navigate to cart automatically")
        
        # FORCE CLICK - This MUST happen automatically, no manual click needed
        print("   🔄 Automatically clicking cart link (no manual click required)...")
        
        # Use JavaScript click as fallback if regular click doesn't work
        try:
            cart_link.click()  # Try regular click first
        except Exception as e:
            print(f"   ⚠️  Regular click failed, trying JavaScript click: {e}")
            self.driver.execute_script("arguments[0].click();", cart_link)
        
        # Small wait to ensure click registered and navigation starts
        time.sleep(0.5)
        
        # Handle any alerts that might appear
        self.handle_alert(accept=True)
        
        # Wait for cart page to load - check for cart page elements
        print("   ⏳ Waiting for cart page to load...")
        try:
            # Wait for URL to change to cart page OR for cart elements to appear
            self.wait.until(
                lambda d: "cart" in d.current_url.lower() or 
                          len(d.find_elements(By.ID, "checkout")) > 0 or
                          len(d.find_elements(By.CLASS_NAME, "cart_item")) > 0
            )
            print("   ✅ Cart page loaded successfully")
        except Exception as e:
            # If timeout, check current URL and try to navigate directly
            current_url = self.driver.current_url
            print(f"   ⚠️  Wait timeout. Current URL: {current_url}")
            if "cart" not in current_url.lower():
                # Try navigating directly to cart
                print("   🔄 Attempting direct navigation to cart page...")
                self.driver.get(self.driver.current_url.split('/inventory')[0] + "/cart.html")
                time.sleep(1)
                # Verify we're on cart page now
                if "cart" in self.driver.current_url.lower():
                    print("   ✅ Cart page loaded via direct navigation")
                else:
                    raise Exception(f"Failed to navigate to cart page. Current URL: {self.driver.current_url}")
            else:
                print("   ✅ Cart page loaded successfully (URL check)")
    
    def add_to_cart_and_go_to_cart(self, product_name: str) -> None:
        """
        Add product to cart and automatically navigate to cart page
        
        This combines adding to cart and going to cart in one automated step
        
        Args:
            product_name: Name of product to add
        """
        self.add_product_to_cart(product_name)
        # Automatically navigate to cart after adding
        self.click_cart_link()
    
    def get_product_price(self, product_name: str) -> str:
        """Get price of specific product"""
        product_card = self.get_product_by_name(product_name)
        price_element = product_card.find_element(*self.PRODUCT_PRICE)
        return price_element.text
