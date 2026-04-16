"""
steps/conftest.py
Provides fixtures for step definitions.
Separating this from the root conftest.py keeps fixture scoping clean.
"""
import pytest
from utils.auth_service import AuthService

@pytest.fixture
def auth() -> AuthService:
    return AuthService()

@pytest.fixture
def context() -> dict:
    return {}
