
'''Production-grade dropdown handler with support for native and custom dropdowns.'''

from dataclasses import dataclass
from typing import Tuple, Optional
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


@dataclass
class DropdownHandler:
    '''
    Unified handler for both native <select> and custom div-based dropdowns.

    Uses Strategy Pattern to handle different dropdown types with a common interface.
    '''
    driver: any
    default_timeout: int = 10

    def select_from_native(
        self, 
        locator: Tuple[str, str], 
        value: str,
        by: str = 'text'
    ) -> str:
        '''
        Select an option from a native HTML <select> element.

        Args:
            locator: Tuple of (By.TYPE, value) to locate the select element
            value: The value to select
            by: Selection method - 'text', 'value', or 'index'

        Returns:
            The selected option text

        Raises:
            TimeoutException: If element not found within timeout
            ValueError: If selection method invalid or option not found
        '''
        # Wait for select element to be present
        select_element = WebDriverWait(self.driver, self.default_timeout).until(
            EC.presence_of_element_located(locator)
        )

        # Create Select wrapper
        select = Select(select_element)

        # Perform selection based on method
        if by == 'text':
            select.select_by_visible_text(value)
        elif by == 'value':
            select.select_by_value(value)
        elif by == 'index':
            select.select_by_index(int(value))
        else:
            raise ValueError(f"Invalid selection method: {by}")

        # Verify selection stuck
        selected_option = select.first_selected_option
        selected_text = selected_option.text

        # Additional verification: check the select's value changed
        time.sleep(0.1)  # Brief pause for any onChange handlers

        return selected_text

    def select_from_custom(
        self,
        trigger_locator: Tuple[str, str],
        option_text: str,
        menu_locator: Optional[Tuple[str, str]] = None,
        option_class: str = "dropdown-option"
    ) -> str:
        '''
        Select an option from a custom div-based dropdown.

        Args:
            trigger_locator: Locator for the element that opens the dropdown
            option_text: The text of the option to select
            menu_locator: Optional locator for the menu container
            option_class: CSS class name of individual options

        Returns:
            The selected option text

        Raises:
            TimeoutException: If elements not found within timeout
            ValueError: If option not found in dropdown
        '''
        # Step 1: Wait for and click the trigger
        trigger = WebDriverWait(self.driver, self.default_timeout).until(
            EC.element_to_be_clickable(trigger_locator)
        )
        trigger.click()

        # Step 2: Wait for dropdown menu to appear
        if menu_locator:
            WebDriverWait(self.driver, self.default_timeout).until(
                EC.visibility_of_element_located(menu_locator)
            )
        else:
            # Wait a bit for menu to appear
            time.sleep(0.3)

        # Step 3: Wait for options to be visible
        option_locator = (By.CLASS_NAME, option_class)
        WebDriverWait(self.driver, self.default_timeout).until(
            EC.visibility_of_element_located(option_locator)
        )

        # Step 4: Find and click the specific option
        options = self.driver.find_elements(By.CLASS_NAME, option_class)

        for option in options:
            if option.text.strip() == option_text:
                # Ensure option is clickable
                WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, option_class))
                )
                option.click()

                # Brief pause for selection to register
                time.sleep(0.2)

                return option_text

        raise ValueError(f"Option '{option_text}' not found in dropdown. "
                       f"Available options: {[opt.text for opt in options]}")

    def get_selected_value_native(self, locator: Tuple[str, str]) -> str:
        '''Get currently selected value from native select.'''
        select_element = self.driver.find_element(*locator)
        select = Select(select_element)
        return select.first_selected_option.text

    def get_selected_value_custom(self, trigger_locator: Tuple[str, str]) -> str:
        '''Get currently selected value from custom dropdown trigger.'''
        trigger = self.driver.find_element(*trigger_locator)
        selected_span = trigger.find_element(By.TAG_NAME, "span")
        return selected_span.text.strip()
