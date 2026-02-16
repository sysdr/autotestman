"""
Test suite for window handling functionality.

Tests verify that window/tab management works correctly in CI/CD environments:
- No race conditions
- Proper cleanup
- URL verification
- Handle isolation
"""

import pytest
import time
from pathlib import Path
from selenium.webdriver.remote.webdriver import WebDriver

from pages.demo_page import DemoPage
from utils.window_manager import WindowManager


class TestWindowHandling:
    """Test suite for window/tab operations."""
    
    @pytest.fixture(autouse=True)
    def setup_demo_page(self, driver: WebDriver, demo_page_url: str):
        """Load demo page before each test."""
        self.page = DemoPage(driver)
        self.page.load(demo_page_url)
        self.driver = driver
    
    def test_open_new_tab_and_verify_url(self):
        """
        Test: Open new tab, verify URL, close it.
        
        This is the core window handling pattern:
        1. Store original state
        2. Trigger new window
        3. Switch using explicit wait
        4. Verify content
        5. Cleanup automatically
        """
        # Record initial state
        original_url = self.page.current_url
        initial_handle_count = len(self.driver.window_handles)
        
        # Measure execution time
        start_time = time.perf_counter()
        
        # Use WindowManager context
        with WindowManager(self.driver, timeout=10) as wm:
            # Trigger new tab
            self.page.click_open_tab_link()
            
            # Switch to new tab (explicit wait, no sleep)
            new_handle = wm.switch_to_new_window()
            
            # Verify we're on the new tab
            assert new_handle != wm.original_window, "Should be on different window"
            assert "new-tab" in self.driver.current_url, "Should be on new tab page"
            
            # Verify content in new tab
            new_page = DemoPage(self.driver)
            title_text = new_page.get_page_title_text()
            assert "New Tab Page" in title_text, f"Expected 'New Tab Page', got '{title_text}'"
        
        # After context exit, verify cleanup
        duration = time.perf_counter() - start_time
        
        # Should be back on original page
        assert self.driver.current_url == original_url, "Should return to original page"
        
        # Should have same number of windows as start
        final_handle_count = len(self.driver.window_handles)
        assert final_handle_count == initial_handle_count,             f"Window leak detected: started with {initial_handle_count}, ended with {final_handle_count}"
        
        # Performance check: should complete in <3 seconds
        assert duration < 3.0, f"Window handling too slow: {duration:.2f}s"
        
        print(f"✓ Test passed in {duration:.2f}s")
    
    def test_open_new_window_and_verify_title(self):
        """Test opening a new window (not tab) and verifying its title."""
        
        original_handle = self.driver.current_window_handle
        
        with WindowManager(self.driver) as wm:
            # Trigger new window
            self.page.click_open_window_link()
            
            # Switch to new window
            wm.switch_to_new_window()
            
            # Verify we're on new window
            assert self.driver.current_window_handle != original_handle
            assert "new-window" in self.driver.current_url
            
            # Verify title
            assert "New Window" in self.driver.title
        
        # Verify restoration
        assert self.driver.current_window_handle == original_handle
    
    def test_multiple_windows_handling(self):
        """Test handling multiple new windows in sequence."""
        
        initial_count = len(self.driver.window_handles)
        
        # Open and close first window
        with WindowManager(self.driver) as wm1:
            self.page.click_open_tab_link()
            wm1.switch_to_new_window()
            assert "new-tab" in self.driver.current_url
        
        # Verify cleanup after first window
        assert len(self.driver.window_handles) == initial_count
        
        # Open and close second window
        with WindowManager(self.driver) as wm2:
            self.page.click_open_window_link()
            wm2.switch_to_new_window()
            assert "new-window" in self.driver.current_url
        
        # Verify final cleanup
        assert len(self.driver.window_handles) == initial_count
    
    def test_window_manager_handles_exceptions(self):
        """Verify cleanup happens even when test fails."""
        
        initial_count = len(self.driver.window_handles)
        
        # Force an exception inside context manager
        with pytest.raises(AssertionError):
            with WindowManager(self.driver) as wm:
                self.page.click_open_tab_link()
                wm.switch_to_new_window()
                
                # This assertion will fail, triggering exception
                assert False, "Forced failure"
        
        # Cleanup should still have happened
        final_count = len(self.driver.window_handles)
        assert final_count == initial_count, "Cleanup failed after exception"


def run_test():
    """Entry point for running tests programmatically."""
    import subprocess
    import sys
    
    result = subprocess.run(
        [sys.executable, "-m", "pytest", __file__, "-v", "--tb=short"],
        capture_output=False
    )
    return result.returncode


if __name__ == "__main__":
    exit(run_test())
