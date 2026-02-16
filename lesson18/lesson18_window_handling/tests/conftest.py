"""
Pytest configuration and fixtures for window handling tests.
"""

import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    """
    Provide a fresh Chrome WebDriver instance for each test.
    
    Configured for CI/CD compatibility:
    - Headless mode (override with HEADED=1 env var)
    - Window size set (avoids responsive layout issues)
    - Disable GPU (prevents crashes in containers)
    """
    import os
    
    options = Options()
    
    # Run headless unless explicitly disabled
    if os.getenv("HEADED") != "1":
        options.add_argument("--headless=new")
    
    # Essential for Docker/CI environments
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # Set consistent window size
    options.add_argument("--window-size=1920,1080")
    
    # Reduce noise in logs
    options.add_argument("--log-level=3")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    
    # Initialize driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    # Set implicit wait (backup for explicit waits)
    driver.implicitly_wait(2)
    
    yield driver
    
    # Cleanup
    driver.quit()


@pytest.fixture(scope="session")
def demo_page_url():
    """
    Provide URL to demo HTML page.
    
    Creates a simple HTTP server for the demo page if needed.
    """
    # For this lesson, we'll use a file:// URL to the demo page
    demo_file = Path(__file__).parent.parent / "demo_page.html"
    
    if not demo_file.exists():
        raise FileNotFoundError(f"Demo page not found at {demo_file}")
    
    return demo_file.as_uri()


@pytest.fixture(autouse=True)
def verify_window_count(driver):
    """
    Automatic fixture that verifies no window leaks after each test.
    
    Production safety check: ensures tests clean up properly.
    """
    initial_count = len(driver.window_handles)
    
    yield
    
    final_count = len(driver.window_handles)
    
    if final_count != initial_count:
        # Force cleanup of leaked windows
        main_handle = driver.window_handles[0]
        for handle in driver.window_handles[1:]:
            driver.switch_to.window(handle)
            driver.close()
        driver.switch_to.window(main_handle)
        
        pytest.fail(
            f"WINDOW LEAK DETECTED: Started with {initial_count} windows, "
            f"ended with {final_count}. Leaked windows were force-closed."
        )
