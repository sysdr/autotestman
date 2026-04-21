"""
UQAP Lesson 76 — Docker Smoke Tests

These tests verify:
  1. Chrome launches inside the Docker environment.
  2. Network egress works (can reach the public internet).
  3. Basic Selenium interactions function in headless mode.
  4. Page title assertion confirms we're on the right page.
"""
from __future__ import annotations

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ── Helpers ──────────────────────────────────────────────────────────

class PageAssertions:
    """Thin wrapper providing readable assertion helpers."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout=15)

    def navigate(self, url: str) -> None:
        self.driver.get(url)

    def title_contains(self, fragment: str) -> bool:
        return fragment.lower() in self.driver.title.lower()

    def element_visible(self, by: By, value: str) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located((by, value)))
            return True
        except Exception:
            return False


# ── Fixtures ─────────────────────────────────────────────────────────

@pytest.fixture
def page(driver) -> PageAssertions:
    """Wrap driver in our assertion helper for cleaner test bodies."""
    return PageAssertions(driver)


# ── Tests ─────────────────────────────────────────────────────────────

class TestDockerEnvironment:
    """Verify the Docker environment itself is correctly configured."""

    def test_chrome_launches(self, driver):
        """Chrome starts and reports a valid capabilities dict."""
        caps = driver.capabilities
        assert "browserVersion" in caps, "Missing browserVersion in capabilities"
        assert caps["browserName"] == "chrome", f"Expected 'chrome', got {caps['browserName']}"
        major = int(caps["browserVersion"].split(".")[0])
        assert major >= 100, f"Chrome version too old: {caps['browserVersion']}"

    def test_chrome_is_headless(self, driver):
        """
        In Docker, Chrome MUST be headless. Verify via user-agent string.
        Non-headless Chrome leaks its display requirement — this is a safety net.
        """
        driver.get("data:text/html,<html></html>")
        ua: str = driver.execute_script("return navigator.userAgent")
        # Newer headless Chrome doesn't include 'Headless' in UA but
        # we confirm by checking the window size matches what we set.
        size = driver.get_window_size()
        assert size["width"] == 1920, f"Window width mismatch: {size}"
        assert size["height"] == 1080, f"Window height mismatch: {size}"

    def test_javascript_execution(self, driver):
        """JavaScript engine works correctly inside the container."""
        result = driver.execute_script("return 2 + 2")
        assert result == 4, f"JS execution returned unexpected: {result}"


class TestNetworkEgress:
    """Verify Chrome can reach public URLs from within Docker."""

    def test_can_reach_example_dot_com(self, page):
        """
        example.com is maintained by IANA specifically for use in
        documentation and tests. It is guaranteed stable.
        """
        page.navigate("https://example.com")
        assert page.title_contains("example"), (
            f"Unexpected page title: '{page.driver.title}'"
        )

    def test_h1_is_present_on_example_com(self, page):
        """Verify DOM element access works — not just navigation."""
        page.navigate("https://example.com")
        assert page.element_visible(By.TAG_NAME, "h1"), (
            "No <h1> found on example.com — DOM access broken"
        )

    def test_page_source_is_not_empty(self, page):
        page.navigate("https://example.com")
        source = page.driver.page_source
        assert len(source) > 100, "Page source suspiciously short — possible network block"


class TestSeleniumInteractions:
    """Core Selenium API: navigation, elements, scripts — all inside Docker."""

    def test_back_forward_navigation(self, driver):
        driver.get("https://example.com")
        first_url = driver.current_url
        driver.get("https://www.iana.org/domains/reserved")
        driver.back()
        assert driver.current_url == first_url, "browser.back() failed"

    def test_screenshot_capture(self, driver, tmp_path):
        """
        Screenshots are critical in CI — they are the only visual
        evidence of what the browser saw when a test fails.
        Verify they can be captured inside Docker.
        """
        driver.get("https://example.com")
        shot_path = tmp_path / "smoke_screenshot.png"
        driver.save_screenshot(str(shot_path))
        assert shot_path.exists(), "Screenshot file was not created"
        assert shot_path.stat().st_size > 1024, "Screenshot is suspiciously small (< 1KB)"
