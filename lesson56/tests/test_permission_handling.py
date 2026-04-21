"""
tests/test_permission_handling.py
Lesson 56: Validates the Two-Layer Permission Strategy.
"""
from __future__ import annotations
import pytest
import logging
from utils.permission_handler import PermissionPopupType, PermissionResult

logger = logging.getLogger(__name__)


class TestPermissionHandling:

    def test_notification_permission_auto_accept(self, android_driver):
        """
        Demonstrates Layer 1 + Layer 2 permission strategy.

        Expected behavior with autoGrantPermissions=True (Layer 1 active):
          - PermissionHandler.handle() returns was_present=False
          - This is CORRECT — popup was pre-granted, test should continue normally

        Expected behavior without Layer 1 (capability disabled):
          - PermissionHandler.handle() returns was_present=True, was_accepted=True
          - Layer 2 caught and handled the popup

        Either outcome = test PASSES.
        """
        driver, handler = android_driver

        # ── Layer 2: Runtime handler (graceful no-op if pre-granted) ──
        result: PermissionResult = handler.handle(PermissionPopupType.NOTIFICATION)

        # ── Assertions ─────────────────────────────────────────────
        # If popup appeared, it must have been accepted
        if result.was_present:
            assert result.was_accepted, (
                "Permission popup appeared but was NOT accepted. "
                "Check locator in permission_handler.py for your Android API level."
            )
            logger.info(f"[OK] Layer 2 handled popup in {result.elapsed_ms:.0f}ms")
        else:
            logger.info("[OK] Layer 1 pre-granted permission — no popup appeared (correct behavior)")

        # ── Verify app reached usable state ────────────────────────
        # Replace with actual element that proves your app's home screen loaded
        # e.g.: driver.find_element(AppiumBy.ID, "com.example.sampleapp:id/home_container")
        logger.info("[OK] App is in usable state post-permission handling")

    def test_multiple_permissions_sequence(self, android_driver):
        """
        Handles camera + notification permissions in one test (common pattern
        for apps that request multiple permissions during onboarding flow).
        """
        driver, handler = android_driver

        results = handler.handle_all([
            PermissionPopupType.NOTIFICATION,
            PermissionPopupType.CAMERA,
        ])

        for result in results:
            if result.was_present:
                assert result.was_accepted, f"Failed to accept {result.popup_type.name} popup"

        accepted_count = sum(1 for r in results if r.was_accepted)
        present_count  = sum(1 for r in results if r.was_present)
        logger.info(
            f"[OK] Handled {present_count} popup(s), accepted {accepted_count}. "
            f"Remaining were pre-granted."
        )

    def test_permission_handler_is_idempotent(self, android_driver):
        """
        Calling handle() twice for the same permission type must not crash.
        Second call should always return was_present=False (already accepted).
        This guards against flaky double-popup edge cases.
        """
        driver, handler = android_driver

        first  = handler.handle(PermissionPopupType.NOTIFICATION)
        second = handler.handle(PermissionPopupType.NOTIFICATION)

        # Second call must never crash, even if popup is gone
        assert not second.was_present, (
            "Notification popup appeared twice — unexpected OS behavior. "
            "Check if app is triggering multiple permission requests."
        )
        logger.info("[OK] PermissionHandler is idempotent — second call gracefully no-oped")
