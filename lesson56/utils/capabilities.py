"""
utils/capabilities.py
Appium capability builders with Layer 1 permission pre-grant.
"""
from __future__ import annotations
from dataclasses import dataclass
from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions


@dataclass
class AndroidCapConfig:
    app_path:     str
    device_name:  str  = "emulator-5554"
    platform_ver: str  = "13.0"
    app_package:  str  = ""
    app_activity: str  = ""


@dataclass
class IOSCapConfig:
    app_path:    str
    device_name: str = "iPhone 14"
    platform_ver: str = "16.0"
    bundle_id:   str = ""


def build_android_options(cfg: AndroidCapConfig) -> UiAutomator2Options:
    options = UiAutomator2Options()
    options.platform_name          = "Android"
    options.platform_version       = cfg.platform_ver
    options.device_name            = cfg.device_name
    options.app                    = cfg.app_path
    options.app_package            = cfg.app_package
    options.app_activity           = cfg.app_activity
    options.no_reset               = False

    # ── Layer 1: Pre-grant all permissions at install time ──────────
    options.set_capability("autoGrantPermissions", True)
    # ───────────────────────────────────────────────────────────────

    options.set_capability("newCommandTimeout", 300)
    options.set_capability("uiautomator2ServerLaunchTimeout", 60000)
    return options


def build_ios_options(cfg: IOSCapConfig) -> XCUITestOptions:
    options = XCUITestOptions()
    options.platform_name    = "iOS"
    options.platform_version = cfg.platform_ver
    options.device_name      = cfg.device_name
    options.app              = cfg.app_path
    options.bundle_id        = cfg.bundle_id

    # ── Layer 1: Auto-accept all iOS system alerts ──────────────────
    options.set_capability("autoAcceptAlerts", True)
    # ───────────────────────────────────────────────────────────────

    options.set_capability("newCommandTimeout", 300)
    return options
