#!/usr/bin/env python3.11
"""
conftest.py — The Hook Engine Room.

This file is invisible to PMs. It is the technical guarantee
that the business prerequisites declared in Background: actually
work, reliably, every time, in any CI environment.

Key design decisions:
  - browser  → scope="session"  : launch once per run (~800ms saved)
  - page     → scope="function" : fresh incognito context per scenario
  - yield    → teardown boundary: cleanup runs even if test crashes
"""
import pytest

try:
    from playwright.sync_api import sync_playwright, Browser, Page
except ModuleNotFoundError as exc:
    raise ImportError(
        "Playwright is not installed for the Python that is running pytest. "
        "Bare `pytest` on PATH often points at ~/.local or the system interpreter, "
        "not this folder's .venv (where setup.py installed playwright).\n\n"
        "  From lesson_64, use one of:\n"
        "    ./run_tests.sh\n"
        "    make test\n"
        "    .venv/bin/python -m pytest tests/\n"
        "    source .venv/bin/activate && pytest tests/"
    ) from exc

BASE_URL = "http://localhost:5001"


@pytest.fixture(scope="session")
def browser_instance():
    """
    Session-scoped fixture: Chromium launches ONCE per test run.

    Launching a full browser binary is expensive (~600-900ms).
    If you put this at function scope, a 50-scenario suite wastes
    ~40 seconds just on browser startups. Never do that.
    """
    with sync_playwright() as playwright:
        browser: Browser = playwright.chromium.launch(headless=True)
        print(f"\n  🌐  Browser launched (session-scoped)")
        yield browser
        browser.close()
        print(f"  🌐  Browser closed (session teardown)")


@pytest.fixture(scope="function")
def page(browser_instance: Browser):
    """
    Function-scoped fixture: a fresh BrowserContext (incognito) per scenario.

    new_context() creates a completely isolated environment:
      - No shared cookies
      - No shared localStorage / sessionStorage
      - No shared authentication state

    This is test isolation without the cost of relaunching the browser.
    It is the pattern that eliminates state leakage between scenarios.
    """
    context = browser_instance.new_context()
    pg: Page = context.new_page()
    yield pg
    # ── TEARDOWN BOUNDARY ──────────────────────────────────
    # Everything below yield runs AFTER each test, even on crash
    context.close()


def pytest_configure(config):
    """Register BDD feature file paths."""
    pass  # pytest-bdd auto-discovers with @scenario decorators
