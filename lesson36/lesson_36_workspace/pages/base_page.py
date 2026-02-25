"""
Base Page Object with common functionality.
"""

from playwright.sync_api import Page
from typing import Optional


class BasePage:
    """Base class for all page objects"""

    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str) -> None:
        """Navigate to a URL"""
        self.page.goto(url)

    def get_local_storage_item(self, key: str) -> Optional[str]:
        """
        Retrieve a value from localStorage.

        This demonstrates that authentication state (stored in localStorage)
        persists across test functions when using storage_state.
        """
        value = self.page.evaluate(f"() => localStorage.getItem('{key}')")
        return value

    def get_cookie(self, name: str) -> Optional[dict]:
        """Retrieve a specific cookie by name"""
        cookies = self.page.context.cookies()
        for cookie in cookies:
            if cookie["name"] == name:
                return cookie
        return None