"""
AlertHandler: Production-grade alert interaction utility.

Features:
- Explicit wait pattern for deterministic behavior
- Context manager for guaranteed cleanup
- Comprehensive logging for debugging
- Type hints for IDE support
"""

from typing import Optional
import logging
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoAlertPresentException


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AlertHandler:
    """
    Context manager for safe alert handling with explicit waits.

    Usage:
        with AlertHandler(driver, timeout=10) as alert:
            text = alert.text
            alert.accept()
    """

    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        Initialize AlertHandler.

        Args:
            driver: Selenium WebDriver instance
            timeout: Maximum seconds to wait for alert (default: 10)
        """
        self.driver = driver
        self.timeout = timeout
        self.alert: Optional[Alert] = None
        logger.info(f"AlertHandler initialized with timeout={timeout}s")

    def __enter__(self) -> Alert:
        """
        Wait for alert to be present and return it.

        Returns:
            Alert: The Selenium Alert object

        Raises:
            TimeoutException: If alert doesn't appear within timeout
        """
        logger.info("Waiting for alert to be present...")
        try:
            wait = WebDriverWait(self.driver, self.timeout)
            self.alert = wait.until(EC.alert_is_present())
            logger.info(f"Alert detected: '{self.alert.text}'")
            return self.alert
        except TimeoutException:
            logger.error(f"Alert did not appear within {self.timeout} seconds")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Ensure alert is dismissed even if exception occurred.

        Returns:
            False to propagate exceptions (we want test failures to be visible)
        """
        if self.alert:
            try:
                # Try to dismiss if still present
                self.alert.dismiss()
                logger.info("Alert dismissed successfully")
            except NoAlertPresentException:
                logger.info("Alert already dismissed")
            except Exception as e:
                logger.warning(f"Error dismissing alert: {e}")

        # Return False to propagate exceptions
        return False


class AlertUtils:
    """Additional utility methods for alert handling."""

    @staticmethod
    def accept_alert(driver: WebDriver, timeout: int = 10) -> str:
        """
        Accept alert and return its text.

        Args:
            driver: Selenium WebDriver instance
            timeout: Maximum seconds to wait

        Returns:
            str: The alert text
        """
        with AlertHandler(driver, timeout) as alert:
            text = alert.text
            alert.accept()
            return text

    @staticmethod
    def dismiss_alert(driver: WebDriver, timeout: int = 10) -> str:
        """
        Dismiss alert and return its text.

        Args:
            driver: Selenium WebDriver instance
            timeout: Maximum seconds to wait

        Returns:
            str: The alert text
        """
        with AlertHandler(driver, timeout) as alert:
            text = alert.text
            alert.dismiss()
            return text

    @staticmethod
    def send_keys_to_prompt(driver: WebDriver, text: str, timeout: int = 10) -> None:
        """
        Send keys to prompt alert and accept.

        Args:
            driver: Selenium WebDriver instance
            text: Text to send to prompt
            timeout: Maximum seconds to wait
        """
        with AlertHandler(driver, timeout) as alert:
            alert.send_keys(text)
            alert.accept()
            logger.info(f"Sent '{text}' to prompt and accepted")