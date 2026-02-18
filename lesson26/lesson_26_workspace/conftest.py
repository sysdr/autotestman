"""
Pytest configuration and hooks for automatic screenshot capture on test failure.
This is the heart of our framework - it intercepts test failures and captures evidence.
"""

import pytest
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from typing import Optional


@pytest.fixture
def driver_init(request):
    """
    Initialize WebDriver and attach it to the test node.
    
    The key insight: we store the driver on request.node so pytest hooks
    can access it later. This is the "dependency injection" pattern.
    """
    options = Options()
    options.add_argument("--headless")  # Run in headless mode for CI/CD
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    
    # CRITICAL: Attach driver to the test node for hook access
    request.node.driver = driver
    request.node.start_time = datetime.now()
    
    yield driver
    
    # Teardown
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook that runs after each test phase (setup/call/teardown).
    
    This is where the magic happens:
    1. We let pytest generate the test report
    2. We check if the test failed
    3. We extract the driver from the test node
    4. We take a screenshot with a unique, timestamped name
    
    The hookwrapper=True pattern allows us to wrap around the report generation.
    The tryfirst=True ensures this runs before other plugins (like pytest-html).
    """
    # Let pytest generate the report first
    outcome = yield
    report = outcome.get_result()
    
    # Only process actual test failures (not setup/teardown)
    if report.when == "call" and report.failed:
        _take_screenshot(item, report)


def _take_screenshot(item, report):
    """
    Capture a screenshot with a unique, contextual filename.
    
    Filename format: test_name_YYYYMMDD_HHMMSS_milliseconds.png
    Directory structure: screenshots/YYYY-MM-DD/
    
    This prevents race conditions and provides forensic context.
    """
    # Safely extract driver (might not exist for non-UI tests)
    driver: Optional[webdriver.Chrome] = getattr(item, "driver", None)
    if not driver:
        return
    
    try:
        # Generate unique filename with millisecond precision
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
        
        # Sanitize test name for filesystem (replace pytest path separators)
        test_name = item.nodeid.replace("::", "_").replace("/", "_").replace(".py", "")
        
        # Create date-based directory structure
        screenshot_dir = Path("screenshots") / datetime.now().strftime("%Y-%m-%d")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        
        # Construct full path
        filepath = screenshot_dir / f"{test_name}_{timestamp}.png"
        
        # Capture screenshot
        driver.save_screenshot(str(filepath))
        
        # Add screenshot path to report for pytest-html integration
        if hasattr(report, "extra"):
            report.extra.append(pytest.html.extras.image(str(filepath)))
        
        print(f"\n📸 Screenshot saved: {filepath}")
        
    except Exception as e:
        # Graceful degradation: don't let screenshot failure break the test report
        print(f"\n⚠️  Screenshot capture failed: {e}")


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "screenshot: mark test to always take screenshot (even on pass)"
    )
