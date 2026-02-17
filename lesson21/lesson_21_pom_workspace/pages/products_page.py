"""
ProductsPage: Page Object for products/inventory page
Represents the page shown after successful login
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from pages.base_page import BasePage


class ProductsPage(BasePage):
    """Page Object representing the products/inventory page."""
    
    # Locators
    PAGE_TITLE = (By.CSS_SELECTOR, ".title")
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    SHOPPING_CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    
    def __init__(self, driver: WebDriver):
        """Initialize ProductsPage"""
        super().__init__(driver)
    
    def is_loaded(self) -> bool:
        """
        Verify products page is loaded.
        
        Returns:
            True if products page is fully loaded
        """
        return (
            self.wait_for_url_contains("inventory.html") and
            self.is_element_visible(self.PAGE_TITLE) and
            self.is_element_visible(self.INVENTORY_CONTAINER)
        )
    
    def get_page_title(self) -> str:
        """
        Get page title text.
        
        Returns:
            Title text (should be "Products")
        """
        return self.get_text(self.PAGE_TITLE)
    
    def get_product_count(self) -> int:
        """
        Get number of products displayed.
        
        Returns:
            Count of product items
        """
        products = self.find_elements(self.PRODUCT_ITEMS)
        return len(products)
    
    def get_cart_item_count(self) -> int:
        """
        Get number of items in cart.
        
        Returns:
            Cart item count (0 if badge not visible)
        """
        if self.is_element_visible(self.SHOPPING_CART_BADGE):
            count_text = self.get_text(self.SHOPPING_CART_BADGE)
            return int(count_text)
        return 0
