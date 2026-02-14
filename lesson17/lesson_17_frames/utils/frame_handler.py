
"""
Frame Context Manager - Production-grade iframe handling
"""
from typing import Union
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchFrameException


class FrameContext:
    """
    Context manager for safe iframe switching with guaranteed cleanup.

    Usage:
        with FrameContext(driver, "iframe-id") as frame:
            # Interact with iframe content
            driver.find_element(By.ID, "input").send_keys("text")
        # Automatically returned to default content
    """

    def __init__(
        self, 
        driver: WebDriver, 
        frame_reference: Union[str, int, WebElement],
        timeout: int = 10
    ):
        """
        Initialize frame context manager.

        Args:
            driver: Selenium WebDriver instance
            frame_reference: Frame identifier (name, id, index, or WebElement)
            timeout: Maximum time to wait for frame availability (seconds)
        """
        self.driver = driver
        self.frame_reference = frame_reference
        self.timeout = timeout
        self._original_context_handles = []

    def __enter__(self):
        """Switch to the specified frame with explicit wait"""
        try:
            # Wait for frame to be available and switch to it
            WebDriverWait(self.driver, self.timeout).until(
                EC.frame_to_be_available_and_switch_to_it(self.frame_reference)
            )
            return self
        except TimeoutException:
            raise NoSuchFrameException(
                f"Frame '{self.frame_reference}' not available within {self.timeout} seconds"
            )

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Always return to default content, even if exception occurred.

        This guarantees no context pollution between tests.
        """
        self.driver.switch_to.default_content()
        # Don't suppress exceptions - let them propagate
        return False


class NestedFrameNavigator:
    """
    Helper for navigating deeply nested frame structures.

    Usage:
        navigator = NestedFrameNavigator(driver)
        navigator.switch_to_path(["outer-frame", "inner-frame"])
        # Interact with content
        navigator.reset()
    """

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
        self.frame_path = []

    def switch_to_path(self, frame_path: list[Union[str, int]]):
        """
        Navigate through a path of nested frames.

        Args:
            frame_path: List of frame references from outermost to innermost
        """
        self.reset()  # Start from clean state

        for frame_ref in frame_path:
            WebDriverWait(self.driver, self.timeout).until(
                EC.frame_to_be_available_and_switch_to_it(frame_ref)
            )
            self.frame_path.append(frame_ref)

    def reset(self):
        """Return to default content and clear path"""
        self.driver.switch_to.default_content()
        self.frame_path = []

    def get_current_depth(self) -> int:
        """Return current nesting depth"""
        return len(self.frame_path)
