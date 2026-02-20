"""
Selenium Login Test - Traditional Approach (For Comparison)
Shows the old way with explicit waits and brittle selectors
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SeleniumLoginTest:
    """Traditional Selenium approach with explicit waits"""
    
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
    
    def test_login_naive(self):
        """
        ❌ ANTI-PATTERN: Using time.sleep()
        This is what junior developers write
        """
        logger.info("Running NAIVE approach (with time.sleep)")
        
        start_time = time.time()
        
        self.driver.get("https://practicetestautomation.com/practice-test-login/")
        time.sleep(3)  # Wait for page to load
        
        username_field = self.driver.find_element(By.ID, "username")
        username_field.send_keys("student")
        time.sleep(1)  # Arbitrary wait
        
        password_field = self.driver.find_element(By.ID, "password")
        password_field.send_keys("Password123")
        time.sleep(1)  # Another arbitrary wait
        
        login_button = self.driver.find_element(By.ID, "submit")
        login_button.click()
        time.sleep(5)  # Wait for redirect
        
        duration = time.time() - start_time
        
        # Verify
        assert "Logged In Successfully" in self.driver.title
        logger.info(f"✅ Naive approach completed in {duration:.2f}s")
        logger.warning(f"⚠️  Wasted {duration - 2:.2f}s on unnecessary waits!")
    
    def test_login_explicit_waits(self):
        """
        ✅ BETTER: Using explicit waits
        But still verbose and error-prone
        """
        logger.info("Running EXPLICIT WAITS approach")
        
        start_time = time.time()
        
        self.driver.get("https://practicetestautomation.com/practice-test-login/")
        
        # Wait for username field to be present
        username_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.send_keys("student")
        
        # Wait for password field to be clickable
        password_field = self.wait.until(
            EC.element_to_be_clickable((By.ID, "password"))
        )
        password_field.send_keys("Password123")
        
        # Wait for button and click
        login_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, "submit"))
        )
        login_button.click()
        
        # Wait for redirect
        self.wait.until(
            EC.url_contains("logged-in-successfully")
        )
        
        duration = time.time() - start_time
        
        assert "Logged In Successfully" in self.driver.title
        logger.info(f"✅ Explicit waits approach completed in {duration:.2f}s")
    
    def cleanup(self):
        """Close the browser"""
        self.driver.quit()


def run_comparison():
    """Run both Selenium approaches and compare"""
    print("\n" + "="*60)
    print("SELENIUM APPROACHES COMPARISON")
    print("="*60 + "\n")
    
    # Test 1: Naive approach
    test1 = SeleniumLoginTest()
    try:
        test1.test_login_naive()
    finally:
        test1.cleanup()
    
    print("\n" + "-"*60 + "\n")
    
    # Test 2: Explicit waits
    test2 = SeleniumLoginTest()
    try:
        test2.test_login_explicit_waits()
    finally:
        test2.cleanup()
    
    print("\n" + "="*60)
    print("KEY OBSERVATIONS:")
    print("1. Naive approach wastes 3-5s on unnecessary sleeps")
    print("2. Explicit waits are better but verbose (3-4 lines per interaction)")
    print("3. Still doesn't handle: animations, overlays, stale elements")
    print("4. Compare this with Playwright's one-line auto-waiting!")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_comparison()
