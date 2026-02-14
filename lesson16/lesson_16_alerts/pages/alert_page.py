"""
AlertDemoPage: Page Object Model for alert testing demo.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path


class AlertDemoPage:
    """Page Object for the alert demo HTML page."""

    # Locators
    JS_ALERT_BUTTON = (By.ID, "jsAlert")
    JS_CONFIRM_BUTTON = (By.ID, "jsConfirm")
    JS_PROMPT_BUTTON = (By.ID, "jsPrompt")
    DELAYED_ALERT_BUTTON = (By.ID, "delayedAlert")
    RESULT_DIV = (By.ID, "result")

    def __init__(self, driver: WebDriver):
        """
        Initialize page object.

        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def load(self):
        """Load the demo page."""
        demo_path = Path(__file__).parent.parent / "demo.html"
        self.driver.get(f"file://{demo_path.absolute()}")
        self.wait.until(EC.presence_of_element_located(self.JS_ALERT_BUTTON))

    def click_js_alert(self):
        """Click the JS Alert button."""
        self.driver.find_element(*self.JS_ALERT_BUTTON).click()

    def click_js_confirm(self):
        """Click the JS Confirm button."""
        self.driver.find_element(*self.JS_CONFIRM_BUTTON).click()

    def click_js_prompt(self):
        """Click the JS Prompt button."""
        self.driver.find_element(*self.JS_PROMPT_BUTTON).click()

    def click_delayed_alert(self):
        """Click the Delayed Alert button."""
        self.driver.find_element(*self.DELAYED_ALERT_BUTTON).click()

    def get_result_text(self) -> str:
        """
        Get the result message text.

        Returns:
            str: The result text
        """
        return self.driver.find_element(*self.RESULT_DIV).text