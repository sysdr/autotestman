
"""
Visual Regression Tests
Demonstrates pixel-perfect screenshot comparison with baseline management.
"""

import pytest
from pathlib import Path
from playwright.sync_api import Page, sync_playwright
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.visual_comparator import VisualRegression


@pytest.fixture(scope="session")
def visual_regression():
    """Fixture providing VisualRegression instance."""
    base_dir = Path(__file__).parent.parent
    baseline_dir = base_dir / "baselines"
    return VisualRegression(baseline_dir=baseline_dir, threshold=0.1)


@pytest.fixture(scope="session")
def browser():
    """Fixture providing Playwright browser instance."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()


def test_homepage_visual(browser, visual_regression):
    """
    Test: Homepage visual regression check.

    Verifies that the Example.com homepage renders consistently.
    First run creates baseline, subsequent runs compare against it.
    """
    base_dir = Path(__file__).parent.parent
    screenshot_dir = base_dir / "screenshots"
    screenshot_dir.mkdir(exist_ok=True)
    diff_dir = base_dir / "diffs"

    # Navigate and capture screenshot
    page = browser.new_page(viewport={"width": 1280, "height": 720})
    page.goto("https://example.com", wait_until="networkidle")

    screenshot_path = screenshot_dir / "homepage.png"
    page.screenshot(path=screenshot_path, full_page=True)
    page.close()

    # Perform visual regression check
    result = visual_regression.compare(
        test_name="homepage",
        current_screenshot=screenshot_path,
        diff_dir=diff_dir
    )

    # Output results
    print(f"\n{result.message}")
    if result.diff_image_path:
        print(f"Diff image saved to: {result.diff_image_path}")

    # Assert test result
    assert result.passed, f"Visual difference {result.diff_percentage:.4f}% exceeds threshold {visual_regression.threshold}%"


def test_responsive_mobile_visual(browser, visual_regression):
    """
    Test: Mobile viewport visual regression check.

    Verifies responsive design at mobile dimensions (375x667).
    """
    base_dir = Path(__file__).parent.parent
    screenshot_dir = base_dir / "screenshots"
    screenshot_dir.mkdir(exist_ok=True)
    diff_dir = base_dir / "diffs"

    # Mobile viewport
    page = browser.new_page(viewport={"width": 375, "height": 667})
    page.goto("https://example.com", wait_until="networkidle")

    screenshot_path = screenshot_dir / "homepage_mobile.png"
    page.screenshot(path=screenshot_path, full_page=True)
    page.close()

    # Perform visual regression check
    result = visual_regression.compare(
        test_name="homepage_mobile",
        current_screenshot=screenshot_path,
        diff_dir=diff_dir
    )

    print(f"\n{result.message}")
    if result.diff_image_path:
        print(f"Diff image saved to: {result.diff_image_path}")

    assert result.passed, f"Visual difference {result.diff_percentage:.4f}% exceeds threshold {visual_regression.threshold}%"
