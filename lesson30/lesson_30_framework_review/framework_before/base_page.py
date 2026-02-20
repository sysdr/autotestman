"""Base page class - before refactoring"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, locator):
        # Find a single element
        return self.driver.find_element(*locator)
    
    def find_elements(self, locator):
        # Find multiple elements
        return self.driver.find_elements(*locator)
    
    def click(self, locator):
        # Click an element
        element = self.wait_for_clickable(locator)
        element.click()
    
    def send_keys(self, locator, text):
        # Type text into element
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def wait_for_element(self, locator, timeout=10):
        # Wait for element to appear
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    def wait_for_clickable(self, locator, timeout=10):
        # Wait for element to be clickable
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    def is_element_present(self, locator):
        # Check if element exists
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    def get_text(self, locator):
        # Get element text
        element = self.find_element(locator)
        return element.text
    
    def get_attribute(self, locator, attribute):
        # Get element attribute value
        element = self.find_element(locator)
        return element.get_attribute(attribute)
