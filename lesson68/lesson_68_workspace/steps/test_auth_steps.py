"""
steps/test_auth_steps.py
Step definitions for User Authentication feature.
Uses a mock AuthService — no browser, no network.
Pure logic: the lesson is about REPORTING, not browser automation.
"""

from __future__ import annotations

import pytest
from pytest_bdd import given, when, then, parsers, scenarios
from utils.auth_service import AuthService, AuthError

# Fixtures live in steps/conftest.py (single definition; avoids duplicate registration).

# Register all scenarios from the feature (paths relative to bdd_features_base_dir in pytest.ini).
scenarios("user_login.feature")


# ─── Given Steps ───────────────────────────────────────────────────────────────

@given("the authentication service is running")
def auth_service_running(auth: AuthService) -> None:
    assert auth.is_healthy(), "AuthService failed health check"

@given("the login form is visible")
def login_form_visible() -> None:
    pass  # UI concern — treated as always true in mock mode

@given(parsers.parse('I have a valid account with username "{username}" and password "{password}"'))
def register_user(auth: AuthService, username: str, password: str) -> None:
    # Idempotent: Background + scenario may both call this for the same user.
    auth.register(username, password)


# ─── When Steps ────────────────────────────────────────────────────────────────

# Regex: Gherkin uses password "" for empty string; parse() does not match that form reliably.
@when(
    parsers.re(
        r'^I submit the login form with username "(?P<username>[^"]*)" and password "(?P<password>[^"]*)"$'
    )
)
def submit_login(auth: AuthService, context: dict, username: str, password: str) -> None:
    try:
        result = auth.login(username, password)
        context["auth_result"] = result
        context["error"] = None
    except AuthError as exc:
        context["auth_result"] = None
        context["error"] = str(exc)

@when(parsers.parse('I fail to login {times:d} times with username "{username}"'))
def fail_login_n_times(auth: AuthService, context: dict, times: int, username: str) -> None:
    for _ in range(times):
        try:
            auth.login(username, "definitely_wrong_password")
        except AuthError as exc:
            context["error"] = str(exc)


# ─── Then Steps ────────────────────────────────────────────────────────────────

@then("I should be redirected to the dashboard")
def assert_dashboard_redirect(context: dict) -> None:
    assert context.get("auth_result") is not None, "Expected successful login"
    assert context["auth_result"].get("redirect") == "/dashboard"

@then(parsers.parse('the welcome banner should display "{message}"'))
def assert_welcome_banner(context: dict, message: str) -> None:
    actual = context["auth_result"].get("welcome")
    assert actual == message, f"Expected '{message}', got '{actual}'"

@then(parsers.parse('I should see the error "{expected_error}"'))
def assert_error_message(context: dict, expected_error: str) -> None:
    actual = context.get("error", "")
    assert actual == expected_error, f"Expected error '{expected_error}', got '{actual}'"

@then("the account should be temporarily locked")
def assert_account_locked(auth: AuthService, context: dict) -> None:
    # After 3 failures, next attempt should raise locked error
    try:
        auth.login("bob", "anypassword")
        pytest.fail("Expected account lock, but login succeeded")
    except AuthError as exc:
        context["error"] = str(exc)
