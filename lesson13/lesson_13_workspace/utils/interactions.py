"""
utils/interactions.py
Production-grade element interaction layer with built-in waits.
"""

from typing import Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class InteractionError(Exception):
    """Raised when element interaction fails after retries."""
    pass


def safe_find_element(
    driver: WebDriver, 
    locator: Tuple[str, str], 
    timeout: int = 10
) -> WebElement:
    """
    Waits for element to be visible in DOM before returning.

    Args:
        driver: WebDriver instance
        locator: Tuple of (By strategy, value) e.g., (By.ID, "username")
        timeout: Maximum seconds to wait

    Returns:
        WebElement when visible

    Raises:
        TimeoutException: If element not visible within timeout
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        print(f"  ✓ Located element: {locator}")
        return element
    except TimeoutException:
        raise TimeoutException(
            f"Element {locator} not visible after {timeout}s"
        )


def type_text(
    driver: WebDriver, 
    locator: Tuple[str, str], 
    text: str, 
    timeout: int = 10,
    clear_first: bool = True
) -> None:
    """
    Safely types text into an input field.

    Args:
        driver: WebDriver instance
        locator: Element locator tuple
        text: Text to type
        timeout: Wait timeout
        clear_first: Clear field before typing
    """
    element = safe_find_element(driver, locator, timeout)

    if clear_first:
        element.clear()

    element.send_keys(text)
    print(f"  ✓ Typed '{text}' into {locator[1]}")


def click_element(
    driver: WebDriver, 
    locator: Tuple[str, str], 
    timeout: int = 10
) -> None:
    """
    Safely clicks an element after waiting for it to be clickable.

    Args:
        driver: WebDriver instance
        locator: Element locator tuple
        timeout: Wait timeout

    Note:
        Uses element_to_be_clickable which checks:
        - Element is visible
        - Element is enabled
        - Element is not obscured by overlays
    """
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        print(f"  ✓ Clicked element: {locator[1]}")
    except TimeoutException:
        raise InteractionError(
            f"Element {locator} not clickable after {timeout}s"
        )


def wait_for_text_in_element(
    driver: WebDriver,
    locator: Tuple[str, str],
    expected_text: str,
    timeout: int = 10
) -> bool:
    """
    Waits for specific text to appear in an element.

    Useful for verifying state changes after actions.
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.text_to_be_present_in_element(locator, expected_text)
        )
        print(f"  ✓ Text '{expected_text}' found in {locator[1]}")
        return True
    except TimeoutException:
        return False