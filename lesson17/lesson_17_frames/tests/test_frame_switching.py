
"""
Frame Switching Tests - Demonstrating production-grade iframe handling
"""
import pytest
from selenium.webdriver.common.by import By
from pages.frame_test_page import FrameTestPage
from utils.frame_handler import FrameContext, NestedFrameNavigator


class TestFrameSwitching:
    """Test suite for frame context switching"""

    def test_main_content_accessible(self, driver, test_page_url):
        """Verify main page content is accessible in default context"""
        driver.get(test_page_url)
        page = FrameTestPage(driver)

        title = page.get_main_title()
        assert title == "Main Page Content"
        assert page.verify_context_is_main()

    def test_switch_to_outer_frame(self, driver, test_page_url):
        """Test switching to outer frame and back"""
        driver.get(test_page_url)
        page = FrameTestPage(driver)

        # Enter text in outer frame
        test_text = "Outer frame test data"
        page.enter_text_in_outer_frame(test_text)

        # Verify we're back in main context
        assert page.verify_context_is_main()

    def test_nested_frame_switching(self, driver, test_page_url):
        """Test switching through nested frames"""
        driver.get(test_page_url)
        page = FrameTestPage(driver)

        # Enter text in deeply nested inner frame
        test_text = "UQAP Testing Framework"
        page.enter_text_in_inner_frame(test_text)

        # Verify text was entered
        stored_value = page.get_inner_frame_input_value()
        assert stored_value == test_text

        # Verify we're back in main context after nested operations
        assert page.verify_context_is_main()

    def test_context_manager_cleanup_on_exception(self, driver, test_page_url):
        """Verify context manager returns to default even when exception occurs"""
        driver.get(test_page_url)

        try:
            with FrameContext(driver, "outerFrame"):
                # Deliberately raise exception inside frame
                raise ValueError("Simulated error")
        except ValueError:
            pass  # Expected

        # Verify we're back in default context despite exception
        main_title = driver.find_element(By.ID, "main-title")
        assert main_title.text == "Main Page Content"

    def test_frame_navigator_path_switching(self, driver, test_page_url):
        """Test NestedFrameNavigator for complex frame paths"""
        driver.get(test_page_url)
        navigator = NestedFrameNavigator(driver)

        # Navigate to nested frame via path
        navigator.switch_to_path(["outerFrame", "innerFrame"])

        # Verify we can interact with inner frame
        inner_input = driver.find_element(By.ID, "inner-input")
        inner_input.send_keys("Path navigation test")

        assert navigator.get_current_depth() == 2

        # Reset to main context
        navigator.reset()
        assert navigator.get_current_depth() == 0

        # Verify in main context
        main_title = driver.find_element(By.ID, "main-title")
        assert main_title is not None

    def test_no_context_pollution_between_tests(self, driver, test_page_url):
        """
        This test must run AFTER test_nested_frame_switching to verify
        that context was properly reset between tests.
        """
        driver.get(test_page_url)

        # If previous test leaked context, this will fail
        main_title = driver.find_element(By.ID, "main-title")
        assert main_title.text == "Main Page Content"
