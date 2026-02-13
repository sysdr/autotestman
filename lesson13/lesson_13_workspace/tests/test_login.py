"""
tests/test_login.py
Production-ready login automation tests.
"""

import pytest
from pages.login_page import LoginPage


class TestLogin:
    """Login functionality test suite."""

    def test_login_with_valid_credentials(self, driver):
        """
        Verify successful login with valid credentials.

        Success Criteria:
        - Username field accepts input
        - Password field accepts input  
        - Submit button is clickable
        - Success message appears within 5s
        """
        page = LoginPage(driver)
        page.navigate()

        page.login(username="testuser", password="password123")

        assert page.is_login_successful(), "Login failed with valid credentials"
        print("\n✓ Test PASSED: Login successful")

    def test_login_with_invalid_credentials(self, driver):
        """Verify error handling for invalid credentials."""
        page = LoginPage(driver)
        page.navigate()

        page.login(username="wronguser", password="wrongpass")

        error_msg = page.get_error_message()
        assert "Invalid credentials" in error_msg, f"Expected error message, got: {error_msg}"
        print("\n✓ Test PASSED: Error message displayed correctly")

    def test_login_with_empty_fields(self, driver):
        """Verify validation for empty fields."""
        page = LoginPage(driver)
        page.navigate()

        page.login(username="", password="")

        error_msg = page.get_error_message()
        assert "required" in error_msg.lower(), f"Expected validation error, got: {error_msg}"
        print("\n✓ Test PASSED: Validation working")