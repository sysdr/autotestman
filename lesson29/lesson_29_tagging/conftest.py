"""
Shared pytest fixtures and hooks
"""
import pytest
from typing import Generator
import time


@pytest.fixture(scope="session")
def test_environment() -> dict:
    """Simulate test environment setup"""
    return {
        "base_url": "https://api.example.com",
        "timeout": 30,
        "retry_count": 3
    }


@pytest.fixture
def api_client(test_environment) -> dict:
    """Mock API client for testing"""
    return {
        "endpoint": test_environment["base_url"],
        "authenticated": True,
        "session_id": "mock-session-123"
    }


@pytest.fixture
def browser_context() -> Generator[dict, None, None]:
    """Simulate browser context (like Playwright)"""
    print("\n🌐 Setting up browser context...")
    context = {
        "browser": "chromium",
        "viewport": {"width": 1920, "height": 1080},
        "user_agent": "pytest-automation"
    }
    yield context
    print("🌐 Tearing down browser context...")


def pytest_collection_modifyitems(config, items):
    """Hook to modify test collection based on markers"""
    # Add custom logic here if needed
    # Example: Skip slow tests in fast mode
    if config.getoption("-m") == "smoke":
        print(f"\n📋 Smoke test mode: {len(items)} tests collected")


def pytest_configure(config):
    """Hook called after command line options are parsed"""
    print("\n" + "="*60)
    print("🚀 UQAP Test Framework - Lesson 29: Tagging & Grouping")
    print("="*60)


def pytest_sessionfinish(session, exitstatus):
    """Hook called after test session finishes"""
    print("\n" + "="*60)
    print(f"✅ Test session completed with exit status: {exitstatus}")
    print("="*60)