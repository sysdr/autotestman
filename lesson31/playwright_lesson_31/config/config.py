"""
Configuration management for UQAP test suite
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import os


@dataclass
class PlaywrightConfig:
    """Centralized configuration for Playwright tests"""
    # Use trailing slash to avoid redirect (todomvc -> todomvc/) which causes "interrupted" errors
    base_url: str = os.getenv("BASE_URL", "https://demo.playwright.dev/todomvc/")
    headless: bool = os.getenv("HEADLESS", "true").lower() == "true"
    timeout: int = int(os.getenv("TIMEOUT", "30000"))
    screenshot_dir: Path = Path("screenshots")
    video_dir: Path = Path("videos")
    trace_dir: Path = Path("traces")
    slow_mo: int = int(os.getenv("SLOW_MO", "0"))
    viewport_width: int = 1920
    viewport_height: int = 1080
    
    # Browser options
    browser_type: str = os.getenv("BROWSER", "chromium")  # chromium, firefox, webkit
    
    # CI/CD specific
    is_ci: bool = os.getenv("CI", "false").lower() == "true"
    retry_count: int = 2 if is_ci else 0
    
    def __post_init__(self):
        """Ensure directories exist"""
        self.screenshot_dir.mkdir(exist_ok=True)
        self.video_dir.mkdir(exist_ok=True)
        self.trace_dir.mkdir(exist_ok=True)


# Singleton instance
config = PlaywrightConfig()
