"""
utils/permission_handler.py
Two-Layer Permission Strategy for UQAP Mobile Automation.
"""
from __future__ import annotations
import logging
from enum import Enum, auto
from dataclasses import dataclass, field

from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)


class PermissionPopupType(Enum):
    NOTIFICATION = auto()
    CAMERA       = auto()
    LOCATION     = auto()
    MICROPHONE   = auto()


class Platform(Enum):
    ANDROID = "android"
    IOS     = "ios"


# ── Locator Registries ─────────────────────────────────────────────
# Android locators vary by API level. We default to API 33+ structure.
_ANDROID_LOCATORS: dict[PermissionPopupType, tuple[str, str]] = {
    PermissionPopupType.NOTIFICATION: (
        AppiumBy.ID,
        "com.android.permissioncontroller:id/permission_allow_button",
    ),
    PermissionPopupType.CAMERA: (
        AppiumBy.ID,
        "com.android.permissioncontroller:id/permission_allow_foreground_only_button",
    ),
    PermissionPopupType.LOCATION: (
        AppiumBy.ID,
        "com.android.permissioncontroller:id/permission_allow_one_time_button",
    ),
    PermissionPopupType.MICROPHONE: (
        AppiumBy.ID,
        "com.android.permissioncontroller:id/permission_allow_button",
    ),
}

_IOS_LOCATORS: dict[PermissionPopupType, tuple[str, str]] = {
    PermissionPopupType.NOTIFICATION: (
        AppiumBy.XPATH,
        "//XCUIElementTypeButton[@name='Allow']",
    ),
    PermissionPopupType.CAMERA: (
        AppiumBy.XPATH,
        "//XCUIElementTypeButton[@name='OK']",
    ),
    PermissionPopupType.LOCATION: (
        AppiumBy.XPATH,
        "//XCUIElementTypeButton[@name='Allow While Using App']",
    ),
    PermissionPopupType.MICROPHONE: (
        AppiumBy.XPATH,
        "//XCUIElementTypeButton[@name='OK']",
    ),
}


@dataclass
class PermissionResult:
    popup_type:   PermissionPopupType
    was_present:  bool
    was_accepted: bool
    elapsed_ms:   float = 0.0

    def __str__(self) -> str:
        status = "ACCEPTED" if self.was_accepted else "NOT PRESENT (pre-granted or N/A)"
        return f"[PermissionResult] {self.popup_type.name}: {status} ({self.elapsed_ms:.0f}ms)"


class PermissionHandler:
    """
    Handles OS-level permission popups using a two-layer strategy:
      Layer 1 — Capability pre-grant (set in driver capabilities, outside this class)
      Layer 2 — Runtime explicit-wait handler (this class)

    A missing popup is NOT a failure — it's logged and the test continues.
    """

    def __init__(
        self,
        driver: WebDriver,
        platform: Platform,
        timeout: float = 5.0,
    ) -> None:
        self.driver   = driver
        self.platform = platform
        self.timeout  = timeout

    def _get_locator(self, popup_type: PermissionPopupType) -> tuple[str, str]:
        registry = (
            _ANDROID_LOCATORS if self.platform == Platform.ANDROID else _IOS_LOCATORS
        )
        if popup_type not in registry:
            raise ValueError(
                f"No locator registered for {popup_type.name} on {self.platform.value}"
            )
        return registry[popup_type]

    def handle(self, popup_type: PermissionPopupType) -> PermissionResult:
        """
        Attempt to locate and accept a permission popup.
        Returns PermissionResult regardless of whether popup appeared.
        """
        import time
        locator = self._get_locator(popup_type)
        start   = time.perf_counter()

        try:
            wait   = WebDriverWait(self.driver, timeout=self.timeout)
            button = wait.until(EC.element_to_be_clickable(locator))
            button.click()
            elapsed = (time.perf_counter() - start) * 1000
            result  = PermissionResult(
                popup_type=popup_type,
                was_present=True,
                was_accepted=True,
                elapsed_ms=elapsed,
            )
            logger.info(f"[OK] {result}")
            return result

        except TimeoutException:
            elapsed = (time.perf_counter() - start) * 1000
            result  = PermissionResult(
                popup_type=popup_type,
                was_present=False,
                was_accepted=False,
                elapsed_ms=elapsed,
            )
            # Not an error — popup was pre-granted or didn't appear
            logger.info(f"[INFO] {result}")
            return result

    def handle_all(
        self, popup_types: list[PermissionPopupType]
    ) -> list[PermissionResult]:
        """Accept multiple permission popups in sequence."""
        return [self.handle(pt) for pt in popup_types]
