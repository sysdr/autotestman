"""
Window Manager - Production-grade window/tab handling for Selenium.

This module provides a context manager for safely handling browser windows/tabs
with guaranteed cleanup and explicit wait strategies.
"""

from typing import Optional, Set
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchWindowException


class WindowManager:
    """
    Context manager for safe window/tab handling.
    
    Features:
    - Automatic cleanup (guaranteed window closure)
    - Explicit waits (no time.sleep)
    - Handle isolation (no index assumptions)
    - Exception-safe (cleanup happens even on errors)
    
    Usage:
        with WindowManager(driver) as wm:
            # Trigger action that opens new window
            driver.find_element(By.ID, "link").click()
            
            # Switch to new window
            wm.switch_to_new_window()
            
            # Interact with new window
            assert "Expected Title" in driver.title
            
        # Automatic cleanup and restoration happens here
    """
    
    def __init__(self, driver: WebDriver, timeout: int = 10) -> None:
        """
        Initialize window manager.
        
        Args:
            driver: Selenium WebDriver instance
            timeout: Maximum seconds to wait for new window (default: 10)
        """
        self.driver: WebDriver = driver
        self.timeout: int = timeout
        self.original_window: Optional[str] = None
        self.new_window: Optional[str] = None
        self._initial_handle_count: int = 0
    
    def __enter__(self) -> 'WindowManager':
        """
        Enter context manager - store original window state.
        
        Returns:
            Self for use in 'with ... as' syntax
        """
        self.original_window = self.driver.current_window_handle
        self._initial_handle_count = len(self.driver.window_handles)
        return self
    
    def switch_to_new_window(self, expected_handle_count: Optional[int] = None) -> str:
        """
        Switch to the newly opened window.
        
        Uses explicit wait to detect new window, then switches to it.
        No index assumptions - uses set difference to find new handle.
        
        Args:
            expected_handle_count: Expected total windows after new one opens.
                                  If None, assumes one new window was opened.
        
        Returns:
            The handle of the new window
            
        Raises:
            TimeoutException: If new window doesn't appear within timeout
            Exception: If new window detection fails
        """
        if expected_handle_count is None:
            expected_handle_count = self._initial_handle_count + 1
        
        # Wait for new window to appear
        try:
            WebDriverWait(self.driver, self.timeout).until(
                lambda d: len(d.window_handles) >= expected_handle_count
            )
        except TimeoutException:
            current_count = len(self.driver.window_handles)
            raise TimeoutException(
                f"New window did not appear within {self.timeout}s. "
                f"Expected {expected_handle_count} windows, found {current_count}"
            )
        
        # Find new window handle via set difference
        current_handles: Set[str] = set(self.driver.window_handles)
        original_handles: Set[str] = {self.original_window}
        new_handles: Set[str] = current_handles - original_handles
        
        if not new_handles:
            raise Exception(
                f"Could not identify new window. "
                f"Current handles: {current_handles}, "
                f"Original: {original_handles}"
            )
        
        # Get the new window handle
        self.new_window = new_handles.pop()
        
        # Switch to new window
        self.driver.switch_to.window(self.new_window)
        
        # Wait for new window to be ready (document.readyState == 'complete')
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        return self.new_window
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """
        Exit context manager - guaranteed cleanup.
        
        Closes new window and restores focus to original window,
        even if an exception occurred.
        
        Args:
            exc_type: Exception type (if any)
            exc_val: Exception value (if any)
            exc_tb: Exception traceback (if any)
            
        Returns:
            False (don't suppress exceptions)
        """
        try:
            # Close new window if it exists and is still open
            if self.new_window:
                current_handles = self.driver.window_handles
                if self.new_window in current_handles:
                    self.driver.switch_to.window(self.new_window)
                    self.driver.close()
            
            # Always restore focus to original window
            if self.original_window in self.driver.window_handles:
                self.driver.switch_to.window(self.original_window)
        except NoSuchWindowException:
            # Original window was closed externally - nothing to restore
            pass
        except Exception as cleanup_error:
            # Log cleanup errors but don't suppress original exception
            print(f"Warning: Cleanup failed: {cleanup_error}")
        
        # Don't suppress exceptions (return False or None)
        return False
