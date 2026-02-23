"""Page Object Model for the User Dashboard."""

from playwright.sync_api import Page, Locator


class DashboardPage:
    """Represents the User Dashboard page."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.url = "http://localhost:8080/app/index.html"

        # Locators
        self.loading_indicator: Locator = page.locator("#loading.active")
        self.user_info: Locator = page.locator("#userInfo.active")
        self.error_message: Locator = page.locator("#errorMessage.active")
        self.error_title: Locator = page.locator("#errorTitle")
        self.error_body: Locator = page.locator("#errorBody")
        self.error_details: Locator = page.locator("#errorDetails")
        self.retry_button: Locator = page.locator("#retryButton")

        # User info elements
        self.user_name: Locator = page.locator("#userName")
        self.user_email: Locator = page.locator("#userEmail")

    def goto(self) -> None:
        """Navigate to the dashboard."""
        self.page.goto(self.url)

    def wait_for_loading(self) -> None:
        """Wait for loading indicator to appear."""
        self.loading_indicator.wait_for(state="visible", timeout=5000)

    def wait_for_user_info(self) -> None:
        """Wait for user info to be displayed."""
        self.user_info.wait_for(state="visible", timeout=5000)

    def wait_for_error(self) -> None:
        """Wait for error message to be displayed."""
        self.error_message.wait_for(state="visible", timeout=5000)

    def is_error_displayed(self) -> bool:
        """Check if error message is visible."""
        return self.error_message.is_visible()

    def get_error_title(self) -> str:
        """Get the error title text."""
        return self.error_title.text_content() or ""

    def get_error_body(self) -> str:
        """Get the error body text."""
        return self.error_body.text_content() or ""

    def get_error_details(self) -> str:
        """Get the error details text."""
        return self.error_details.text_content() or ""

    def click_retry(self) -> None:
        """Click the retry button."""
        self.retry_button.click()

    def is_retry_enabled(self) -> bool:
        """Check if retry button is enabled."""
        return self.retry_button.is_enabled()
