"""
Playwright Login Test - Modern Async/Await Approach
Demonstrates auto-waiting locators without explicit waits
"""

import pytest
import asyncio
import logging
from pathlib import Path
from playwright.async_api import async_playwright, Page, Browser
from pages.login_page import LoginPage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Slow down execution so you can watch each step (milliseconds between actions)
SLOW_MO_MS = 1000
STEP_PAUSE_SEC = 1.5


class TestLoginPlaywright:
    """Test suite using Playwright's async API"""
    
    @pytest.mark.asyncio
    async def test_login_with_valid_credentials(self):
        """
        Test successful login with valid credentials
        Notice: Zero explicit waits, yet stable execution
        """
        async with async_playwright() as p:
            # Launch browser (slow_mo adds delay between each Playwright action)
            browser = await p.chromium.launch(headless=False, slow_mo=SLOW_MO_MS)
            page = await browser.new_page()
            
            try:
                login_page = LoginPage(page)
                
                await login_page.navigate()
                await asyncio.sleep(STEP_PAUSE_SEC)
                
                await login_page.login(
                    username="student",
                    password="Password123"
                )
                await asyncio.sleep(STEP_PAUSE_SEC)
                
                is_logged_in = await login_page.is_logged_in()
                assert is_logged_in, "Login failed - dashboard not visible"
                
                page_title = await page.title()
                assert "Logged In Successfully" in page_title or "Practice Test Automation" in page_title
                
                logger.info("✅ Test passed: Login successful")
                await asyncio.sleep(STEP_PAUSE_SEC)
                
            finally:
                await browser.close()
    
    @pytest.mark.asyncio
    async def test_login_with_invalid_credentials(self):
        """Test login failure with invalid credentials"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, slow_mo=SLOW_MO_MS)
            page = await browser.new_page()
            
            try:
                login_page = LoginPage(page)
                await login_page.navigate()
                await asyncio.sleep(STEP_PAUSE_SEC)
                
                await login_page.login(
                    username="wronguser",
                    password="wrongpass"
                )
                await asyncio.sleep(STEP_PAUSE_SEC)
                
                error_msg = await login_page.get_error_message()
                assert error_msg is not None, "Expected error message not displayed"
                
                logger.info(f"✅ Test passed: Error displayed - {error_msg}")
                await asyncio.sleep(STEP_PAUSE_SEC)
                
            finally:
                await browser.close()


# Standalone execution for demonstration
async def run_demo():
    """Run a demo test outside pytest"""
    print(f"\n{Colors.BOLD}🎭 Running Playwright Demo{Colors.END}\n")
    
    start_time = asyncio.get_event_loop().time()
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=SLOW_MO_MS)
        page = await browser.new_page()
        
        login_page = LoginPage(page)
        await login_page.navigate()
        
        print(f"{Colors.YELLOW}⏳ Attempting login...{Colors.END}")
        await login_page.login("student", "Password123")
        
        is_logged_in = await login_page.is_logged_in()
        
        end_time = asyncio.get_event_loop().time()
        duration = end_time - start_time
        
        if is_logged_in:
            print(f"{Colors.GREEN}✅ Login successful in {duration:.2f}s{Colors.END}")
        else:
            print(f"{Colors.RED}❌ Login failed{Colors.END}")
        
        await asyncio.sleep(2)  # Show result
        await browser.close()


class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'


if __name__ == "__main__":
    asyncio.run(run_demo())
