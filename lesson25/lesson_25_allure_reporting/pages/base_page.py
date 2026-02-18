"""Base Page Object with Allure integration"""
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    @allure.step("Navigate to {url}")
    def navigate(self, url: str) -> None:
        """Navigate to a URL with Allure step logging"""
        self.driver.get(url)
    
    @allure.step("Find element: {locator}")
    def find_element(self, locator: tuple):
        """Find element with wait and Allure logging"""
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="element_not_found",
                attachment_type=allure.attachment_type.PNG
            )
            raise
    
    @allure.step("Click element: {locator}")
    def click(self, locator: tuple) -> None:
        """Click element with Allure step"""
        element = self.find_element(locator)
        element.click()
    
    @allure.step("Enter text '{text}' into {locator}")
    def enter_text(self, locator: tuple, text: str) -> None:
        """Enter text with Allure step"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
