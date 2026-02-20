"""
Base Page Object - Foundation for all page classes
"""
import asyncio
from playwright.async_api import Page, Locator, expect
from typing import Optional
from pathlib import Path
from config import config


class BasePage:
    """Base class for all page objects"""
    
    def __init__(self, page: Page):
        self.page = page
        self.config = config
    
    async def navigate(self, url: Optional[str] = None):
        """Navigate to URL (uses base_url if not provided). Retries once on transient network errors."""
        target_url = url or self.config.base_url
        last_error = None
        retry_indicators = ("err_connection_reset", "interrupted", "chromewebdata")
        for attempt in range(3):
            try:
                await self.page.goto(target_url, wait_until="domcontentloaded", timeout=self.config.timeout)
                return
            except Exception as e:
                last_error = e
                err_lower = str(e).lower()
                if attempt < 2 and any(s in err_lower for s in retry_indicators):
                    await asyncio.sleep(1)  # Brief pause before retry
                    continue
                raise
        raise last_error
    
    async def wait_for_element(self, locator: Locator, timeout: Optional[int] = None):
        """Wait for element to be visible"""
        await locator.wait_for(state="visible", timeout=timeout or self.config.timeout)
    
    async def take_screenshot(self, name: str):
        """Take screenshot and save to configured directory"""
        screenshot_path = self.config.screenshot_dir / f"{name}.png"
        await self.page.screenshot(path=str(screenshot_path))
        return screenshot_path
    
    async def get_title(self) -> str:
        """Get page title"""
        return await self.page.title()
    
    async def get_url(self) -> str:
        """Get current URL"""
        return self.page.url
