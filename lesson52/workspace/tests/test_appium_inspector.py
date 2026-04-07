"""
test_appium_inspector.py — Pytest suite for Lesson 52.

Runs in two modes:
  DEMO_MODE=true  → parses local XML fixture (no Appium server needed)
  DEMO_MODE=false → connects to real Appium session
"""
import os
import pytest
from pathlib import Path
import sys

# Ensure workspace root is on path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "utils"))
sys.path.insert(0, str(ROOT / "config"))

DEMO_MODE = os.environ.get("DEMO_MODE", "true").lower() == "true"


# ── Fixtures ──────────────────────────────────────────────────────────────
@pytest.fixture(scope="module")
def inspector():
    """
    Returns either an OfflineInspector (demo) or a live AppiumInspector.
    Yielding allows teardown (session quit) after all tests in the module.
    """
    from inspector import AppiumInspector, OfflineInspector

    if DEMO_MODE:
        xml_fixture = ROOT / "fixtures" / "login_screen.xml"
        yield OfflineInspector(xml_fixture)
        return

    # Live Appium session setup
    from appium import webdriver
    from appium.options import UiAutomator2Options
    import appium_caps as caps

    options = UiAutomator2Options()
    options.platform_name     = caps.PLATFORM_NAME
    options.device_name       = caps.DEVICE_NAME
    options.app               = caps.APK_PATH
    options.app_package       = caps.APP_PACKAGE
    options.app_activity      = caps.APP_ACTIVITY
    options.new_command_timeout = caps.NEW_COMMAND_TIMEOUT
    options.app_wait_duration = caps.APP_WAIT_DURATION

    driver = webdriver.Remote(caps.APPIUM_HOST, options=options)
    yield AppiumInspector(driver)
    driver.quit()


# ── Tests ─────────────────────────────────────────────────────────────────
def test_login_button_is_discoverable(inspector):
    """
    Core test: confirm the Login button can be found by text.
    Fails with a descriptive message rather than a generic exception.
    """
    result = inspector.find_by_text("Login")
    assert result is not None, (
        "Login button NOT FOUND on screen by text='Login'. "
        "Check app state — is the Login activity the first screen?"
    )


def test_login_button_has_resource_id(inspector):
    """
    Validate the Login button has a resource-id (required for stable automation).
    A missing resource-id is a red flag — report it to the dev team.
    """
    result = inspector.find_by_text("Login")
    assert result is not None, "Login button not found — run test_login_button_is_discoverable first"
    assert result.resource_id, (
        f"Login button found (text='Login') but has NO resource-id! "
        f"Element: class={result.class_name}, bounds={result.bounds}. "
        f"Ask the dev team to add android:id='@+id/btn_login' to the layout."
    )


def test_login_button_is_clickable(inspector):
    """Confirm the element reports itself as clickable."""
    result = inspector.find_by_text("Login")
    assert result is not None
    assert result.clickable, (
        f"Login button found but clickable=False! "
        f"resource-id: {result.resource_id}. The button may be disabled on load."
    )


def test_locator_file_is_generated(inspector, tmp_path):
    """
    End-to-end test: inspect → write locators.py → verify file contents.
    This is the full Inspector-as-Code pipeline in miniature.
    """
    from inspector import AppiumInspector
    output_file = tmp_path / "login_screen_locators.py"

    login_btn = inspector.find_by_text("Login")
    AppiumInspector.write_locators(
        {"LOGIN_BUTTON": login_btn},
        output_file,
        build_version="test-build-001",
    )

    assert output_file.exists(), "Locator file was not created"
    content = output_file.read_text()
    assert "LOGIN_BUTTON_ID" in content,   "resource-id var missing from locators file"
    assert "DO NOT EDIT MANUALLY" in content, "Header comment missing"
    assert "com.example.myapp:id/btn_login" in content, "Expected resource-id not in file"


def test_all_buttons_discoverable(inspector):
    """Audit: find ALL buttons on screen. Useful for full-screen inspection reports."""
    buttons = inspector.find_all_buttons()
    assert len(buttons) > 0, "No Button widgets found on screen at all"
    button_texts = [b.text for b in buttons]
    assert "Login" in button_texts, (
        f"Login not among discovered buttons. Found: {button_texts}"
    )
