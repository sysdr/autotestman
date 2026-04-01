# conftest.py
import pytest
from playwright.async_api import async_playwright, APIRequestContext
from typing import AsyncGenerator

@pytest.fixture(scope="function")
async def playwright_instance():
    """Playwright instance — used to create API request contexts."""
    async with async_playwright() as p:
        yield p

@pytest.fixture(scope="function")
async def api_context(playwright_instance) -> AsyncGenerator[APIRequestContext, None]:
    """
    APIRequestContext is Playwright's lightweight HTTP client.
    It skips rendering, JavaScript execution, and CSS — perfect for link checking.
    A new context per test function ensures isolation.
    """
    context = await playwright_instance.request.new_context(
        ignore_https_errors=True,
        extra_http_headers={"User-Agent": "UQAP-FastChecker/1.0"},
    )
    yield context
    await context.dispose()
