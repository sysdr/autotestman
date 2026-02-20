"""
Login Page Object Model
Demonstrates Playwright's locator-based approach
"""

import asyncio
from playwright.async_api import Page, expect
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Pause between actions so you can watch the flow (seconds)
ACTION_DELAY_SEC = 0.8


class LoginPage:
    """Page Object for the login page with auto-waiting locators"""
    
    def __init__(self, page: Page):
        self.page = page
        
        # Define locators (lazy, not queried until action)
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")
        # Practice site: Submit is a <button id="submit"> — use button selector so we click the actual button
        self.login_button = page.locator("button#submit")
        # Error message is in div#error (practice site)
        self.error_message = page.locator("div#error")
        self.success_indicator = page.locator("h1:has-text('Logged In Successfully')")
    
    async def navigate(self, url: str = "https://practicetestautomation.com/practice-test-login/") -> None:
        """Navigate to the login page"""
        logger.info(f"Navigating to: {url}")
        await self.page.goto(url, wait_until="domcontentloaded")
    
    async def login(self, username: str, password: str) -> None:
        """
        Perform login action
        Auto-waits for elements to be actionable
        """
        logger.info(f"Logging in with username: {username}")
        
        # Auto-waiting: Playwright checks if element is:
        # 1. Attached to DOM
        # 2. Visible
        # 3. Stable (not animating)
        # 4. Enabled
        # 5. Not obscured
        await self.username_input.fill(username)
        logger.debug("Username filled")
        await asyncio.sleep(ACTION_DELAY_SEC)

        await self.password_input.fill(password)
        logger.debug("Password filled")
        await asyncio.sleep(ACTION_DELAY_SEC)

        # Ensure Submit button is in view and click it (practice site uses <button id="submit">)
        await self.login_button.scroll_into_view_if_needed()
        await self.login_button.click()
        logger.debug("Login button clicked")
        await asyncio.sleep(ACTION_DELAY_SEC)

    async def get_error_message(self) -> Optional[str]:
        """Get error message if present"""
        try:
            await self.error_message.wait_for(state="visible", timeout=5000)
            return await self.error_message.text_content()
        except Exception:
            return None

    async def is_on_login_page(self) -> bool:
        """True if still on the login page (no redirect to success)."""
        return "practice-test-login" in self.page.url and "logged-in-successfully" not in self.page.url
    
    async def is_logged_in(self) -> bool:
        """Check if login was successful by checking for dashboard elements"""
        try:
            await self.success_indicator.wait_for(state="visible", timeout=5000)
            current_url = self.page.url
            logger.info(f"Login successful, redirected to: {current_url}")
            return True
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            return False
