
'''Page Object for the dropdown test page.'''

from selenium.webdriver.common.by import By
from utils.dropdown_handler import DropdownHandler
from typing import Tuple


class DropdownTestPage:
    '''Page Object encapsulating dropdown test page interactions.'''

    # Locators
    NATIVE_SELECT = (By.ID, "country-select")
    NATIVE_RESULT = (By.ID, "native-result")

    CUSTOM_TRIGGER = (By.ID, "custom-trigger")
    CUSTOM_MENU = (By.ID, "custom-menu")
    CUSTOM_SELECTED = (By.ID, "custom-selected")
    CUSTOM_RESULT = (By.ID, "custom-result")

    def __init__(self, driver):
        self.driver = driver
        self.dropdown_handler = DropdownHandler(driver)

    def select_country(self, country: str) -> str:
        '''Select a country from the native dropdown.'''
        return self.dropdown_handler.select_from_native(
            self.NATIVE_SELECT,
            country,
            by='text'
        )

    def select_custom_option(self, option: str) -> str:
        '''Select an option from the custom dropdown.'''
        return self.dropdown_handler.select_from_custom(
            trigger_locator=self.CUSTOM_TRIGGER,
            option_text=option,
            menu_locator=self.CUSTOM_MENU,
            option_class="dropdown-option"
        )

    def get_native_result(self) -> str:
        '''Get the displayed result for native select.'''
        result_element = self.driver.find_element(*self.NATIVE_RESULT)
        return result_element.text

    def get_custom_result(self) -> str:
        '''Get the displayed result for custom dropdown.'''
        result_element = self.driver.find_element(*self.CUSTOM_RESULT)
        return result_element.text

    def verify_native_selection(self, expected: str) -> bool:
        '''Verify the native dropdown has the expected selection.'''
        selected = self.dropdown_handler.get_selected_value_native(self.NATIVE_SELECT)
        return selected == expected

    def verify_custom_selection(self, expected: str) -> bool:
        '''Verify the custom dropdown has the expected selection.'''
        selected = self.dropdown_handler.get_selected_value_custom(self.CUSTOM_TRIGGER)
        return selected == expected
