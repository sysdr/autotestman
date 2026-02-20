"""
Login functionality tests
Demonstrates smoke vs regression test categorization
"""
import pytest
import time


@pytest.mark.smoke
@pytest.mark.ui
def test_user_can_login_with_valid_credentials(browser_context):
    """Critical path: User login with valid credentials"""
    print("\n  🔐 Testing login with valid credentials...")
    time.sleep(0.1)  # Simulate UI interaction

    username = "test_user@example.com"
    password = "SecurePass123!"

    # Simulate login process
    assert username, "Username should not be empty"
    assert password, "Password should not be empty"
    assert browser_context["browser"] == "chromium"

    print("  ✓ Login successful")


@pytest.mark.smoke
@pytest.mark.api
def test_login_api_returns_token(api_client):
    """Critical path: API authentication returns valid token"""
    print("\n  🔑 Testing API token generation...")
    time.sleep(0.05)

    response = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "expires_in": 3600,
        "user_id": "12345"
    }

    assert response["token"], "Token should be present"
    assert response["expires_in"] > 0, "Token expiry should be positive"
    assert api_client["authenticated"], "Client should be authenticated"

    print("  ✓ Token generated successfully")


@pytest.mark.regression
@pytest.mark.ui
def test_login_fails_with_invalid_password(browser_context):
    """Edge case: Login with wrong password"""
    print("\n  🚫 Testing login with invalid password...")
    time.sleep(0.1)

    username = "test_user@example.com"
    password = "WrongPassword"

    # Simulate failed login
    error_message = "Invalid credentials"
    assert error_message == "Invalid credentials"

    print("  ✓ Proper error handling verified")


@pytest.mark.regression
@pytest.mark.ui
def test_login_blocked_after_multiple_failures(browser_context):
    """Edge case: Account lockout after failed attempts"""
    print("\n  🔒 Testing account lockout mechanism...")
    time.sleep(0.15)

    failed_attempts = 5
    max_attempts = 5

    assert failed_attempts >= max_attempts, "Should trigger lockout"

    print("  ✓ Account lockout working correctly")


@pytest.mark.regression
@pytest.mark.slow
def test_login_with_expired_session():
    """Edge case: Handling expired sessions"""
    print("\n  ⏱️  Testing expired session handling...")
    time.sleep(0.2)  # Simulate slow operation

    session_age_hours = 25
    max_session_hours = 24

    assert session_age_hours > max_session_hours, "Session should be expired"

    print("  ✓ Expired session handled correctly")