"""
Browser Factory Utility
Provides reusable browser configurations for tests
"""

from playwright.async_api import async_playwright, Browser, Page, BrowserContext
from typing import Optional, Dict, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class BrowserConfig:
    """Configuration for browser instances"""
    headless: bool = False
    slow_mo: int = 0
    viewport: Dict[str, int] = None
    user_agent: Optional[str] = None
    
    def __post_init__(self):
        if self.viewport is None:
            self.viewport = {"width": 1280, "height": 720}


class BrowserFactory:
    """Factory for creating configured browser instances"""
    
    @staticmethod
    async def create_browser(
        browser_type: str = "chromium",
        config: Optional[BrowserConfig] = None
    ) -> Browser:
        """
        Create a browser instance with specified configuration
        
        Args:
            browser_type: chromium, firefox, or webkit
            config: BrowserConfig instance
        
        Returns:
            Browser instance
        """
        if config is None:
            config = BrowserConfig()
        
        playwright = await async_playwright().start()
        
        browser_args = {
            "headless": config.headless,
            "slow_mo": config.slow_mo
        }
        
        if browser_type == "chromium":
            browser = await playwright.chromium.launch(**browser_args)
        elif browser_type == "firefox":
            browser = await playwright.firefox.launch(**browser_args)
        elif browser_type == "webkit":
            browser = await playwright.webkit.launch(**browser_args)
        else:
            raise ValueError(f"Unknown browser type: {browser_type}")
        
        logger.info(f"Launched {browser_type} browser")
        return browser
    
    @staticmethod
    async def create_context(
        browser: Browser,
        config: Optional[BrowserConfig] = None
    ) -> BrowserContext:
        """Create a browser context with configuration"""
        if config is None:
            config = BrowserConfig()
        
        context = await browser.new_context(
            viewport=config.viewport,
            user_agent=config.user_agent
        )
        
        return context
