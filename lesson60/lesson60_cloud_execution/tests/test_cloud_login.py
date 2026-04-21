"""
tests/test_cloud_login.py — UQAP Lesson 60
Real test against BrowserStack's demo Android app.
Tests are cloud-backend agnostic — they use fixtures, not driver details.
"""
from __future__ import annotations
import os
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WAIT = 15   # seconds — cloud devices can be 3–5s slower than localhost


class TestCloudAppLaunch:
    """Verify the app launches and key UI elements are present on cloud."""

    def test_app_launch_on_cloud(self, mobile_driver):
        """
        GIVEN  the BrowserStack demo app is installed on a real device
        WHEN   the session starts
        THEN   the login screen renders within 15 seconds
        """
        wait = WebDriverWait(mobile_driver, WAIT)

        # BrowserStack demo app shows a login screen on launch
        # Using explicit wait — NEVER time.sleep() here
        login_input = wait.until(
            EC.presence_of_element_located(
                (AppiumBy.ACCESSIBILITY_ID, "Username")
            )
        )
        assert login_input.is_displayed(), "Login input not visible"

    def test_successful_login(self, mobile_driver):
        """
        GIVEN  the app is at the login screen
        WHEN   valid credentials are entered
        THEN   the dashboard screen is displayed
        """
        wait = WebDriverWait(mobile_driver, WAIT)

        username_field = wait.until(
            EC.element_to_be_clickable(
                (AppiumBy.ACCESSIBILITY_ID, "Username")
            )
        )
        username_field.click()
        username_field.send_keys("alice@example.com")

        password_field = mobile_driver.find_element(
            AppiumBy.ACCESSIBILITY_ID, "Password"
        )
        password_field.send_keys("test@123")

        login_btn = mobile_driver.find_element(
            AppiumBy.ACCESSIBILITY_ID, "Log In"
        )
        login_btn.click()

        # Verify dashboard appeared
        dashboard = wait.until(
            EC.presence_of_element_located(
                (AppiumBy.XPATH, "//*[@text='Dashboard']")
            )
        )
        assert dashboard.is_displayed(), "Dashboard not shown after login"

    def test_session_metadata(self, mobile_driver):
        """
        Verify session has expected cloud metadata.
        This catches capability misconfiguration silently.
        """
        caps = mobile_driver.capabilities
        platform = caps.get("platformName", "").lower()
        assert platform == "android", (
            f"Expected Android, got '{platform}'. "
            "Check your capability configuration."
        )
        # Verify we're on a real device, not a misconfigured local run
        udid = caps.get("udid", "")
        assert len(udid) > 5, "UDID missing — may not be running on cloud device"
