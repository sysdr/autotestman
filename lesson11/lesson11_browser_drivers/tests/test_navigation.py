"""
Test: Browser Navigation
Demonstrates proper browser automation with explicit waits.
"""

import sys
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.driver_manager import DriverManager
from pages.google_page import GoogleHomePage


def run_test(headless: bool = False, keep_open_seconds: int = 0) -> bool:
    """
    Execute the navigation test.
    
    Args:
        headless: Run in headless mode (no visible browser)
        keep_open_seconds: Keep browser open for this many seconds (0 = close immediately)
        
    Returns:
        True if test passed
    """
    print("\n" + "="*60)
    print("Lesson 11: Browser Drivers & Navigation Test")
    print("="*60 + "\n")
    
    driver_manager = DriverManager(headless=headless)
    
    try:
        # Step 1: Initialize driver
        print("[SETUP] Initializing Chrome WebDriver...")
        driver = driver_manager.get_driver()
        print(f"[INFO] Driver initialized: {driver.capabilities['browserVersion']}")
        
        # Step 2: Navigate using Page Object
        print("[ACTION] Navigating to Google...")
        page = GoogleHomePage(driver)
        page.load()
        
        # Step 3: Get page title
        title = page.get_title()
        print(f"[RESULT] Page Title: '{title}'")
        
        # Step 4: Verify
        assert page.verify_loaded(), "Page verification failed"
        assert "Google" in title, f"Expected 'Google' in title, got '{title}'"
        
        print("[PASS] ✓ All assertions passed")
        
        # Optional: Keep browser open for inspection
        if keep_open_seconds > 0:
            print(f"[INFO] Keeping browser open for {keep_open_seconds} seconds for inspection...")
            time.sleep(keep_open_seconds)
        
        return True
        
    except Exception as e:
        print(f"[FAIL] ✗ Test failed: {e}")
        return False
        
    finally:
        # Step 5: Cleanup
        print("[CLEANUP] Closing browser...")
        driver_manager.quit_driver()
        print("="*60 + "\n")


def verify_result(keep_open_seconds: int = 0) -> None:
    """
    Verification function to check test success.
    Demonstrates both headless and headed modes.
    
    Args:
        keep_open_seconds: Keep browser open for this many seconds (0 = close immediately)
    """
    print("Running test in HEADED mode (you'll see the browser)...")
    result_headed = run_test(headless=False, keep_open_seconds=keep_open_seconds)
    
    print("\n" + "-"*60 + "\n")
    
    print("Running test in HEADLESS mode (no visible browser)...")
    result_headless = run_test(headless=True, keep_open_seconds=0)  # No need to keep headless open
    
    print("\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    print(f"Headed Mode:   {'PASS ✓' if result_headed else 'FAIL ✗'}")
    print(f"Headless Mode: {'PASS ✓' if result_headless else 'FAIL ✗'}")
    print("="*60 + "\n")
    
    if result_headed and result_headless:
        print("🎉 All tests passed! Your browser automation is production-ready.")
    else:
        print("⚠️  Some tests failed. Review the logs above.")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run browser navigation test")
    parser.add_argument(
        "--keep-open",
        type=int,
        default=0,
        help="Keep browser open for N seconds after test completes (default: 0 = close immediately)"
    )
    args = parser.parse_args()
    
    verify_result(keep_open_seconds=args.keep_open)
