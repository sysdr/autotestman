
'''Custom wait conditions for complex UI interactions.'''

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from typing import Tuple, Callable


def wait_for_dropdown_expanded(driver, menu_locator: Tuple, timeout: int = 10) -> bool:
    '''
    Waits for a custom dropdown menu to be fully expanded and ready.

    Verifies:
    1. Menu container is visible
    2. Menu has non-zero height (CSS animations complete)
    3. At least one option is present
    '''
    def condition(driver):
        try:
            menu = driver.find_element(*menu_locator)
            if not menu.is_displayed():
                return False

            # Check menu has rendered height
            height = menu.size['height']
            if height <= 0:
                return False

            # Check options are present
            options = menu.find_elements(menu_locator[0], f"{menu_locator[1]} .dropdown-option")
            return len(options) > 0
        except (StaleElementReferenceException, NoSuchElementException):
            return False

    WebDriverWait(driver, timeout).until(condition)
    return True


def wait_for_element_stable(driver, locator: Tuple, timeout: int = 10) -> bool:
    '''
    Waits for an element's position and size to stabilize.
    Useful for elements affected by CSS animations or dynamic layouts.
    '''
    def condition(driver):
        try:
            element = driver.find_element(*locator)
            initial_location = element.location
            initial_size = element.size

            # Wait a bit and check again
            driver.implicitly_wait(0.1)

            current_location = element.location
            current_size = element.size

            return (initial_location == current_location and 
                   initial_size == current_size)
        except (StaleElementReferenceException, NoSuchElementException):
            return False

    WebDriverWait(driver, timeout).until(condition)
    return True


class ElementTextMatches:
    '''Custom expected condition: element text matches expected value.'''

    def __init__(self, locator: Tuple, expected_text: str):
        self.locator = locator
        self.expected_text = expected_text

    def __call__(self, driver):
        try:
            element = driver.find_element(*self.locator)
            return element.text.strip() == self.expected_text
        except (StaleElementReferenceException, NoSuchElementException):
            return False
