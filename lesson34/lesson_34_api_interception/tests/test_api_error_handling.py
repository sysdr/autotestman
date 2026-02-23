"""Test suite for API error handling using network interception."""

import pytest
from playwright.sync_api import Page

from pages.dashboard_page import DashboardPage
from utils.network_mock import NetworkInterceptor


class TestAPIErrorHandling:
    """Test error handling for various API failure scenarios."""

    @pytest.fixture
    def dashboard(self, page: Page) -> DashboardPage:
        """Create a DashboardPage instance."""
        return DashboardPage(page)

    def test_500_server_error_shows_message(
        self, page: Page, dashboard: DashboardPage
    ) -> None:
        """Test that 500 errors display appropriate error message."""
        # Intercept API and return 500 error
        with NetworkInterceptor.mock_api_response(
            page,
            "**/api/users/**",
            status=500,
            body={"error": "Internal Server Error"},
        ):
            dashboard.goto()
            dashboard.wait_for_error()

        # Verify error UI is displayed
        assert dashboard.is_error_displayed(), "Error message should be visible"

        error_title = dashboard.get_error_title()
        assert "Server Error" in error_title, (
            f"Expected 'Server Error' in title, got: {error_title}"
        )

        error_body = dashboard.get_error_body()
        assert "experiencing issues" in error_body.lower(), (
            "Error body should mention server issues"
        )

        error_details = dashboard.get_error_details()
        assert "500" in error_details, "Error details should show 500 status code"

    def test_404_not_found_shows_message(
        self, page: Page, dashboard: DashboardPage
    ) -> None:
        """Test that 404 errors display not found message."""
        with NetworkInterceptor.mock_api_response(
            page,
            "**/api/users/**",
            status=404,
            body={"error": "User not found"},
        ):
            dashboard.goto()
            dashboard.wait_for_error()

        assert dashboard.is_error_displayed()

        error_title = dashboard.get_error_title()
        assert "Not Found" in error_title

        error_body = dashboard.get_error_body()
        assert "not found" in error_body.lower()

    def test_401_unauthorized_shows_message(
        self, page: Page, dashboard: DashboardPage
    ) -> None:
        """Test that 401 errors display authentication message."""
        with NetworkInterceptor.mock_api_response(
            page,
            "**/api/users/**",
            status=401,
            body={"error": "Unauthorized"},
        ):
            dashboard.goto()
            dashboard.wait_for_error()

        assert dashboard.is_error_displayed()

        error_title = dashboard.get_error_title()
        assert "Unauthorized" in error_title

        error_body = dashboard.get_error_body()
        assert "log in" in error_body.lower()

    def test_network_timeout_shows_connection_error(
        self, page: Page, dashboard: DashboardPage
    ) -> None:
        """Test that network timeouts display connection error."""
        with NetworkInterceptor.mock_network_failure(
            page,
            "**/api/users/**",
            error="failed",
        ):
            dashboard.goto()
            dashboard.wait_for_error()

        assert dashboard.is_error_displayed()

        error_title = dashboard.get_error_title()
        assert "Connection Failed" in error_title or "Unexpected Error" in error_title

        error_details = dashboard.get_error_details()
        assert "Failed to fetch" in error_details or "Network" in error_details

    def test_retry_button_enabled_on_error(
        self, page: Page, dashboard: DashboardPage
    ) -> None:
        """Test that retry button is enabled when error occurs."""
        with NetworkInterceptor.mock_api_response(
            page, "**/api/users/**", status=500
        ):
            dashboard.goto()
            dashboard.wait_for_error()

        assert dashboard.is_retry_enabled(), "Retry button should be enabled"

    def test_multiple_error_scenarios_in_sequence(
        self, page: Page, dashboard: DashboardPage
    ) -> None:
        """Test that different errors can be handled in sequence."""
        # First: 500 error
        with NetworkInterceptor.mock_api_response(
            page, "**/api/users/**", status=500
        ):
            dashboard.goto()
            dashboard.wait_for_error()
            error_title_1 = dashboard.get_error_title()
            assert "Server Error" in error_title_1

        # Then: 404 error after retry
        with NetworkInterceptor.mock_api_response(
            page, "**/api/users/**", status=404
        ):
            dashboard.click_retry()
            dashboard.wait_for_error()
            error_title_2 = dashboard.get_error_title()
            assert "Not Found" in error_title_2


def test_successful_request_without_interception(page: Page) -> None:
    """Verify app works normally without interception (baseline test)."""
    dashboard = DashboardPage(page)
    dashboard.goto()

    # Without interception, the real API should work
    dashboard.wait_for_user_info()

    # Verify user data is displayed
    user_name = dashboard.user_name.text_content()
    assert user_name, "User name should be displayed"
    assert len(user_name) > 0, "User name should not be empty"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
