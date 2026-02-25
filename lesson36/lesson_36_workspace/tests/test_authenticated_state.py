"""
Test Suite: Authenticated State Storage Demonstration

This test suite demonstrates the UQAP pattern for authentication caching:
1. First test triggers authentication (via session-scoped fixture)
2. Auth state is saved to auth_state.json
3. All subsequent tests load the saved state (no re-authentication)

Run with: pytest tests/ -v -s
"""

import pytest
from pages.dashboard_page import DashboardPage
from playwright.sync_api import Page


class TestAuthenticatedState:
    """Tests demonstrating storage state reuse"""

    def test_01_verify_authentication_state_loaded(
        self, authenticated_page: Page
    ) -> None:
        """
        Test: Verify that authentication state is pre-loaded.

        Expected Behavior:
            - No login flow executed
            - localStorage contains auth_token
            - Cookies contain session_id
        """
        dashboard = DashboardPage(authenticated_page)
        dashboard.load()

        # Verify authentication via localStorage
        assert dashboard.is_authenticated(), "Auth token not found in localStorage"

        # Verify user data was loaded
        user_id = dashboard.get_user_id()
        assert user_id == "42", f"Expected user_id=42, got {user_id}"

        print(f"\n✓ User authenticated with ID: {user_id}")

    def test_02_verify_user_role_persists(
        self, authenticated_page: Page
    ) -> None:
        """
        Test: Verify that user role persists across tests.

        Engineering Note:
            This test runs AFTER test_01, but it doesn't re-authenticate.
            The storage state is already loaded from auth_state.json.
        """
        dashboard = DashboardPage(authenticated_page)
        dashboard.load()

        role = dashboard.get_user_role()
        assert role == "admin", f"Expected role=admin, got {role}"

        print(f"\n✓ User role verified: {role}")

    def test_03_verify_cookies_present(
        self, authenticated_page: Page
    ) -> None:
        """
        Test: Verify that authentication cookies are injected.

        This demonstrates that both localStorage AND cookies are restored
        from the saved storage state.
        """
        dashboard = DashboardPage(authenticated_page)
        dashboard.load()

        # Check for session cookie
        session_cookie = dashboard.get_cookie("session_id")
        assert session_cookie is not None, "Session cookie not found"
        assert session_cookie["value"] == "abc123xyz789"

        # Check for auth token cookie
        auth_cookie = dashboard.get_cookie("auth_token")
        assert auth_cookie is not None, "Auth token cookie not found"
        assert auth_cookie["httpOnly"] is True, "Auth cookie should be httpOnly"

        print(f"\n✓ Cookies verified: {len(authenticated_page.context.cookies())} cookies loaded")

    def test_04_multiple_pages_share_state(
        self, authenticated_page: Page
    ) -> None:
        """
        Test: Verify that state persists across multiple page navigations.

        This simulates a user clicking through the app—authentication
        should remain valid throughout the session.
        """
        dashboard = DashboardPage(authenticated_page)

        # Navigate to first page
        dashboard.load()
        assert dashboard.is_authenticated()

        # Navigate away and back
        authenticated_page.goto("https://demo.playwright.dev/")
        authenticated_page.goto(dashboard.URL)

        # Verify authentication still valid
        assert dashboard.is_authenticated(), "Auth lost after navigation"

        print("\n✓ Authentication persists across page navigations")


class TestPerformanceComparison:
    """Demonstrating the performance benefit"""

    def test_measure_state_loading_speed(
        self, authenticated_page: Page
    ) -> None:
        """
        Test: Measure how fast state loading is vs. full login.

        Expected Result:
            Loading saved state takes ~50ms
            Full login would take 2-3 seconds
        """
        import time

        start = time.time()
        dashboard = DashboardPage(authenticated_page)
        dashboard.load()
        assert dashboard.is_authenticated()
        elapsed = time.time() - start

        print(f"\n⏱️  State load + page load: {elapsed:.3f}s")
        assert elapsed < 2.0, "State loading should be sub-2 seconds"