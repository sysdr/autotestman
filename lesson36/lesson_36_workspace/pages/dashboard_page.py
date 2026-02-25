"""
Dashboard Page Object - represents authenticated user dashboard.
"""

from playwright.sync_api import Page
from .base_page import BasePage


class DashboardPage(BasePage):
    """Page object for the main dashboard"""

    URL = "https://demo.playwright.dev/api-mocking/"

    def __init__(self, page: Page):
        super().__init__(page)

    def load(self) -> None:
        """Navigate to dashboard"""
        self.navigate(self.URL)

    def is_authenticated(self) -> bool:
        """
        Check if user is authenticated by verifying storage state.

        Returns:
            True if auth_token exists in localStorage
        """
        auth_token = self.get_local_storage_item("auth_token")
        return auth_token is not None

    def get_user_id(self) -> str:
        """Get the authenticated user's ID from localStorage"""
        user_id = self.get_local_storage_item("user_id")
        return user_id or "unknown"

    def get_user_role(self) -> str:
        """Get the authenticated user's role"""
        role = self.get_local_storage_item("user_role")
        return role or "guest"