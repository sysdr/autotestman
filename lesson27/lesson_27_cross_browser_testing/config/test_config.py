"""
Test Configuration Module
=========================
Centralized configuration for cross-browser testing.
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class CrossBrowserTestConfig:
    """Main test configuration for cross-browser tests."""
    
    # Browser to test (Chrome only)
    browsers: List[str] = field(default_factory=lambda: ["chrome"])
    
    # Test URL
    base_url: str = "https://the-internet.herokuapp.com"
    
    # Execution settings
    headless: bool = False
    parallel: bool = False
    max_workers: int = 3
    
    # Timeouts
    default_timeout: int = 10
    page_load_timeout: int = 30
    
    # Reporting
    generate_html_report: bool = True
    screenshot_on_failure: bool = True
    
    def get_browser_options(self, browser: str) -> Dict[str, Any]:
        """Get Chrome options."""
        if browser == "chrome":
            return {
                "disable-extensions": "",
                "disable-popup-blocking": "",
            }
        return {}


# Global config instance
config = CrossBrowserTestConfig()
