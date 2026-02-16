"""
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
        # Use alert handling in case there's a security dialog
        self.wait_and_click_with_alert_handling(self.CONTINUE_BUTTON)
        # Wait for checkout overview page to load after clicking continue
        self.wait_and_find(self.FINISH_BUTTON)
    
    def finish_checkout(self) -> None:
        """Complete the purchase"""
        # Use alert handling in case there's a security dialog
        self.wait_and_click_with_alert_handling(self.FINISH_BUTTON)
    
    def get_success_message(self) -> str:
        """Get order completion message"""
        return self.get_element_text(self.SUCCESS_MESSAGE)
    
    def is_checkout_complete(self) -> bool:
        """Verify checkout completed successfully"""
        return self.wait_for_url_contains("/checkout-complete.html")
