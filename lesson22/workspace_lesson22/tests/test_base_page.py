"""
Test demonstrating BasePage pattern
Uses a real demo site to show inheritance in action
"""

import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.profile_page import ProfilePage


class TestBasePagePattern:
    """Test suite demonstrating BasePage benefits"""
    
    BASE_URL = "https://the-internet.herokuapp.com"
    
    def test_login_flow(self, driver):
        """
        Test complete login flow using BasePage methods
        Demonstrates zero code duplication across pages
        """
        # Navigate to login page
        driver.get(f"{self.BASE_URL}/login")
        
        # Use LoginPage (inherits from BasePage)
        login_page = LoginPage(driver)
        login_page.login("tomsmith", "SuperSecretPassword!")
        
        # Verify redirect (simple validation)
        assert "/secure" in driver.current_url
        
        print("✓ Login flow completed using BasePage methods")
    
    def test_failed_login_with_error_handling(self, driver):
        """
        Test that BasePage error handling works
        """
        driver.get(f"{self.BASE_URL}/login")
        
        login_page = LoginPage(driver)
        login_page.login("invalid_user", "invalid_pass")
        
        # BasePage's _find handles wait automatically
        # No time.sleep() needed!
        assert login_page.is_error_displayed()
        
        print("✓ Error handling works via BasePage")
    
    def test_dynamic_content_wait(self, driver):
        """
        Test that explicit waits handle dynamic content
        This would fail with time.sleep() approach
        """
        driver.get(f"{self.BASE_URL}/dynamic_loading/1")
        
        # Click start button
        from selenium.webdriver.common.by import By
        from core.base_page import BasePage
        
        page = BasePage(driver)
        page._click((By.CSS_SELECTOR, "#start button"))
        
        # Wait for dynamic content (appears after 5s)
        # BasePage's _find waits automatically
        finish_text = page._get_text((By.ID, "finish"))
        assert "Hello World!" in finish_text
        
        print("✓ Dynamic content handled without sleep()")


def run_test():
    """Main entry point for visualization"""
    print("\n" + "="*60)
    print("LESSON 22: Abstracting the Base Page - Demo")
    print("="*60 + "\n")
    
    # Run pytest programmatically
    import sys
    sys.exit(pytest.main([__file__, "-v", "-s"]))


def verify_result():
    """Verify the lesson implementation"""
    from pathlib import Path
    
    checks = {
        "BasePage exists": Path("core/base_page.py").exists(),
        "LoginPage inherits": "BasePage" in Path("pages/login_page.py").read_text(),
        "No time.sleep": "time.sleep" not in Path("pages/login_page.py").read_text(),
        "Tests exist": Path("tests/test_base_page.py").exists(),
    }
    
    print("\n" + "="*60)
    print("VERIFICATION RESULTS")
    print("="*60)
    
    for check, result in checks.items():
        status = "✓" if result else "✗"
        print(f"{status} {check}")
    
    all_passed = all(checks.values())
    print("\n" + ("🎉 All checks passed!" if all_passed else "❌ Some checks failed"))
    
    return all_passed


if __name__ == "__main__":
    run_test()
