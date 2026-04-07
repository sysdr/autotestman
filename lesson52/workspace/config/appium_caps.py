"""
Appium desired capabilities for UIAutomator2.
Adjust APP_PACKAGE and APP_ACTIVITY to match your APK.
"""
from pathlib import Path

# ── Emulator / Device ──────────────────────────────────────────────────────
PLATFORM_NAME    = "Android"
DEVICE_NAME      = "emulator-5554"        # `adb devices` to confirm
AUTOMATION_NAME  = "UiAutomator2"
PLATFORM_VERSION = "13"                    # Match your AVD API level

# ── APK ────────────────────────────────────────────────────────────────────
APK_PATH = str(Path(__file__).parent.parent / "apks" / "app-debug.apk")

# If APK is already installed, use package + activity instead:
APP_PACKAGE  = "com.example.myapp"
APP_ACTIVITY = ".ui.login.LoginActivity"

# ── Appium Server ──────────────────────────────────────────────────────────
APPIUM_HOST = "http://127.0.0.1:4723"

# ── Timeouts ───────────────────────────────────────────────────────────────
NEW_COMMAND_TIMEOUT = 60   # seconds before Appium kills idle session
APP_WAIT_DURATION   = 10   # seconds to wait for activity to appear
