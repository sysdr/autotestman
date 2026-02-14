
"""
Page Object for frame testing page
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.frame_handler import FrameContext, NestedFrameNavigator


class FrameTestPage:
    """Page object encapsulating frame interaction logic"""

    # Main page locators
    MAIN_TITLE = (By.ID, "main-title")
    MAIN_MESSAGE = (By.ID, "main-message")
    MAIN_BUTTON = (By.ID, "main-button")

    # Outer frame locators
    OUTER_FRAME = (By.ID, "outerFrame")
    OUTER_TITLE = (By.ID, "outer-title")
    OUTER_INPUT = (By.ID, "outer-input")
    OUTER_BUTTON = (By.ID, "outer-button")

    # Inner frame locators
    INNER_FRAME = (By.ID, "innerFrame")
    INNER_TITLE = (By.ID, "inner-title")
    INNER_INPUT = (By.ID, "inner-input")
    INNER_BUTTON = (By.ID, "inner-button")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def get_main_title(self) -> str:
        """Get title from main page (default context)"""
        element = self.wait.until(EC.presence_of_element_located(self.MAIN_TITLE))
        return element.text

    def enter_text_in_outer_frame(self, text: str):
        """Enter text in outer frame input field"""
        with FrameContext(self.driver, self.OUTER_FRAME):
            input_field = self.wait.until(
                EC.presence_of_element_located(self.OUTER_INPUT)
            )
            input_field.clear()
            input_field.send_keys(text)

    def get_outer_frame_title(self) -> str:
        """Get title from outer frame"""
        with FrameContext(self.driver, self.OUTER_FRAME):
            element = self.wait.until(
                EC.presence_of_element_located(self.OUTER_TITLE)
            )
            return element.text

    def enter_text_in_inner_frame(self, text: str):
        """Enter text in nested inner frame"""
        # Navigate through outer frame to inner frame
        with FrameContext(self.driver, self.OUTER_FRAME):
            with FrameContext(self.driver, self.INNER_FRAME):
                input_field = self.wait.until(
                    EC.presence_of_element_located(self.INNER_INPUT)
                )
                input_field.clear()
                input_field.send_keys(text)

    def get_inner_frame_input_value(self) -> str:
        """Get value from inner frame input field"""
        with FrameContext(self.driver, self.OUTER_FRAME):
            with FrameContext(self.driver, self.INNER_FRAME):
                input_field = self.wait.until(
                    EC.presence_of_element_located(self.INNER_INPUT)
                )
                return input_field.get_attribute("value")

    def verify_context_is_main(self) -> bool:
        """Verify driver is in main/default context"""
        try:
            self.driver.find_element(*self.MAIN_TITLE)
            return True
        except:
            return False
