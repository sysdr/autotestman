"""
Pytest configuration and fixtures
This is the heart of the test infrastructure
"""
import pytest
import asyncio
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from pages.todo_page import TodoPage
from config import config
from pathlib import Path
from datetime import datetime


@pytest.fixture(scope="function")
async def browser():
    """
    Function-scoped browser so it runs in the same event loop as tests.
    Session scope + async causes event-loop mismatch and hangs with pytest-asyncio.
    """
    async with async_playwright() as playwright:
        browser_type = getattr(playwright, config.browser_type)
        launch_opts = {"headless": config.headless, "slow_mo": config.slow_mo}
        if config.headless and config.browser_type == "chromium":
            launch_opts["args"] = ["--no-sandbox", "--disable-setuid-sandbox"]
        browser = await browser_type.launch(**launch_opts)
        yield browser
        await browser.close()


@pytest.fixture(scope="function")
async def context(browser: Browser):
    """
    Function-scoped context for test isolation
    Each test gets a fresh context (cookies, storage, etc.)
    """
    context = await browser.new_context(
        viewport={"width": config.viewport_width, "height": config.viewport_height},
        record_video_dir=str(config.video_dir) if not config.is_ci else None,
    )
    yield context
    await context.close()


@pytest.fixture(scope="function")
async def page(context: BrowserContext):
    """
    Function-scoped page
    Each test gets a fresh page
    """
    page = await context.new_page()
    yield page
    await page.close()


@pytest.fixture(scope="function")
async def todo_page(page: Page):
    """
    TodoPage instance ready to use
    Automatically navigates to base URL
    """
    todo_page = TodoPage(page)
    await todo_page.navigate()
    return todo_page


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Pytest hook to capture test results
    Takes screenshot on failure
    """
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Test failed - capture screenshot
        try:
            page = item.funcargs.get("page")
        except Exception:
            page = None
        if page:
            screenshot_name = f"failure_{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            screenshot_path = config.screenshot_dir / f"{screenshot_name}.png"
            try:
                loop = asyncio.get_event_loop()
                loop.run_until_complete(page.screenshot(path=str(screenshot_path)))
                print(f"Screenshot saved: {screenshot_path}")
            except Exception as e:
                print(f"Screenshot capture failed: {e}")


def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", 'slow: marks tests as slow (deselect with \'-m "not slow"\')')
    config.addinivalue_line("markers", "smoke: marks tests as smoke tests")
    config.addinivalue_line("markers", "regression: marks tests as regression tests")
