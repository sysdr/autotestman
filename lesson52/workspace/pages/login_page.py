"""
login_page.py — Page Object for the Login Screen.

Imports locators from the auto-generated file. If the locator file
doesn't exist yet, it falls back to text-based lookup (less stable,
but still beats a hardcoded string).
"""
from __future__ import annotations
from pathlib import Path
import sys
import logging

logger = logging.getLogger(__name__)

# Attempt to load generated locators; fall back to defaults
try:
    sys.path.insert(0, str(Path(__file__).parent.parent / "locators"))
    from login_screen_locators import (   # type: ignore[import]
        LOGIN_BUTTON_ID,
        LOGIN_BUTTON_TEXT,
    )
    logger.info("Using generated locators: LOGIN_BUTTON_ID=%s", LOGIN_BUTTON_ID)
except ImportError:
    LOGIN_BUTTON_ID   = None
    LOGIN_BUTTON_TEXT = "Login"
    logger.warning("Generated locators not found; falling back to text='Login'")


class LoginPage:
    """Encapsulates all interactions with the Login screen."""

    def __init__(self, driver) -> None:
        self._driver = driver

    def _find_login_button(self):
        from appium.webdriver.common.appiumby import AppiumBy

        # Prefer resource-id (stable), fall back to text (fragile but workable)
        if LOGIN_BUTTON_ID:
            return self._driver.find_element(AppiumBy.ID, LOGIN_BUTTON_ID)
        return self._driver.find_element(AppiumBy.XPATH, f'//android.widget.Button[@text="{LOGIN_BUTTON_TEXT}"]')

    def tap_login(self) -> None:
        """Tap the Login button."""
        self._find_login_button().click()

    def is_login_button_visible(self) -> bool:
        """Non-throwing check — returns True if button is on screen."""
        try:
            btn = self._find_login_button()
            return btn.is_displayed()
        except Exception:
            return False
