"""
conftest.py — Pytest fixtures for Lesson 44.
Demonstrates fixture chaining: api_client → created_user → test.
"""
import sys
from pathlib import Path

# Ensure workspace root is on path so "utils" resolves when run from any cwd
_workspace_root = Path(__file__).resolve().parent.parent
if str(_workspace_root) not in sys.path:
    sys.path.insert(0, str(_workspace_root))

import pytest
from utils.api_client import ApiClient, UserResponse


BASE_URL = "http://localhost:8000"


@pytest.fixture(scope="session")
def api_client() -> ApiClient:
    """
    Session-scoped: one HTTP client for the entire test run.
    Expensive to create; safe to share since it holds no mutable test state.
    """
    client = ApiClient(base_url=BASE_URL)
    yield client
    client.close()


@pytest.fixture
def created_user(api_client: ApiClient) -> UserResponse:
    """
    Function-scoped (default): fresh user per test.
    yield = guaranteed teardown even if the test raises an exception.
    """
    user = api_client.create_user(name="Alice", email="alice@uqap.test")
    print(f"\n  [SETUP]    POST /users → id={user.id}")
    yield user
    print(f"  [TEARDOWN] DELETE /users/{user.id}")
    api_client.delete_user(user.id)
