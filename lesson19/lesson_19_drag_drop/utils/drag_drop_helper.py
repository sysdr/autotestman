"""
utils/drag_drop_helper.py
Production-grade drag-and-drop handler with retry logic.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    StaleElementReferenceException,
    MoveTargetOutOfBoundsException,
    ElementNotInteractableException
)
import time
from typing import Tuple


class DragDropHelper:
    """Handles drag-and-drop operations with retry logic and explicit waits."""

    def __init__(self, driver: WebDriver, wait_timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, wait_timeout)
        self.actions = ActionChains(driver)

    def drag_and_drop_with_retry(
        self, 
        source_locator: Tuple[str, str], 
        target_locator: Tuple[str, str],
        max_attempts: int = 3
    ) -> bool:
        """
        Perform drag-and-drop with retry logic.

        Args:
            source_locator: Tuple of (By.TYPE, "value") for source element
            target_locator: Tuple of (By.TYPE, "value") for target element
            max_attempts: Maximum retry attempts

        Returns:
            True if successful, raises exception otherwise
        """
        for attempt in range(max_attempts):
            try:
                # Wait for elements to be visible
                print(f"         → Attempt {attempt + 1}: Waiting for source element...")
                source = self.wait.until(
                    EC.visibility_of_element_located(source_locator)
                )
                print(f"         → Source element found!")
                
                print(f"         → Waiting for target element...")
                target = self.wait.until(
                    EC.visibility_of_element_located(target_locator)
                )
                print(f"         → Target element found!")

                # Scroll source into view (critical for headless)
                print(f"         → Scrolling source element into view...")
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", 
                    source
                )
                time.sleep(0.2)  # Let scroll complete

                # Execute drag with explicit pauses
                print(f"         → Clicking and holding source element...")
                self.actions.click_and_hold(source).pause(0.3)
                print(f"         → Moving to target element...")
                self.actions.move_to_element(target).pause(0.2)
                print(f"         → Releasing...")
                self.actions.release().perform()
                print(f"         → Action chain completed!")

                print(f"      ✅ Drag-and-drop successful (attempt {attempt + 1})")
                return True

            except (StaleElementReferenceException, 
                    MoveTargetOutOfBoundsException,
                    ElementNotInteractableException) as e:
                print(f"⚠️  Attempt {attempt + 1} failed: {type(e).__name__}")

                if attempt == max_attempts - 1:
                    raise

                # Reset action chain and backoff
                self.actions.reset_actions()
                backoff_delay = 0.5 * (attempt + 1)
                time.sleep(backoff_delay)

        return False

    def verify_element_in_container(
        self, 
        element_id: str, 
        container_id: str
    ) -> bool:
        """
        Verify element is inside container using JavaScript.

        Args:
            element_id: ID of element to check
            container_id: ID of container element

        Returns:
            True if element is inside container
        """
        script = f"""
        return document.querySelector('#{container_id}')
                      .contains(document.querySelector('#{element_id}'));
        """
        return self.driver.execute_script(script)