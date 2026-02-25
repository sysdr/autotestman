"""
Pytest fixtures for authenticated state management.
This demonstrates the production pattern for authentication caching.
"""

import pytest
from pathlib import Path
from playwright.sync_api import Browser, Page, BrowserContext


@pytest.fixture(scope="session")
def authenticated_state_file(browser: Browser) -> str:
    """
    Session-scoped fixture: Authenticate ONCE and save state.

    Returns:
        Path to the saved authentication state file.

    Engineering Note:
        - scope="session" means this runs once per pytest invocation
        - The state file is reused across ALL tests
        - If the file exists, we skip authentication entirely
    """
    state_file = Path(__file__).parent/ "auth_state.json"

    # Optimization: Reuse existing state if available
    if state_file.exists():
        print(f"\n🔄 Reusing existing auth state from {state_file}")
        return str(state_file)

    print(f"\n🔐 No auth state found. Authenticating...")

    # Create a temporary context for login
    context = browser.new_context()
    page = context.new_page()

    try:
        # Perform authentication flow
        page.goto("https://demo.playwright.dev/api-mocking/")

        # Simulate a login by setting localStorage (this is a demo)
        page.evaluate("""
            () => {
                localStorage.setItem('auth_token', 'demo_token_xyz_123');
                localStorage.setItem('user_id', '42');
                localStorage.setItem('user_role', 'admin');
            }
        """)

        # Set authentication cookies
        context.add_cookies([
            {
                "name": "session_id",
                "value": "abc123xyz789",
                "domain": "demo.playwright.dev",
                "path": "/",
            },
            {
                "name": "auth_token",
                "value": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.demo",
                "domain": "demo.playwright.dev",
                "path": "/",
                "httpOnly": True,
                "secure": True,
            },
        ])

        # CRITICAL: Capture the authenticated state
        context.storage_state(path=str(state_file))
        print_success(f"✓ Auth state saved to {state_file}")

    finally:
        context.close()

    return str(state_file)


@pytest.fixture
def authenticated_context(
    browser: Browser, 
    authenticated_state_file: str
) -> BrowserContext:
    """
    Function-scoped fixture: Create a context with pre-loaded auth.

    Args:
        browser: Playwright browser instance
        authenticated_state_file: Path to saved state (from session fixture)

    Returns:
        Browser context with authentication already loaded

    Engineering Note:
        - This fixture runs for EACH test
        - The context is created with storage_state parameter
        - Playwright injects cookies + localStorage before first navigation
    """
    context = browser.new_context(storage_state=authenticated_state_file)
    yield context
    context.close()


@pytest.fixture
def authenticated_page(authenticated_context: BrowserContext) -> Page:
    """
    Convenience fixture: Pre-authenticated page ready for testing.

    Returns:
        Page object with authentication state loaded
    """
    page = authenticated_context.new_page()
    yield page
    page.close()


def print_success(message: str) -> None:
    """Helper for colored output"""
    GREEN = "\033[92m"
    END = "\033[0m"
    print(f"{GREEN}{message}{END}")