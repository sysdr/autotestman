#!/usr/bin/env python3.11
"""
Step definitions for login.feature.

Notice:
  - @given("the application is running") and
  - @given("I am on the login page")
  are defined ONCE here. The Background: block in the
  .feature file wires them to every scenario automatically.

  You do NOT need to tag them with any scenario. pytest-bdd
  resolves them by text matching.
"""
import pytest
from pytest_bdd import given, when, then, scenario, parsers
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:5001"
FEATURE  = "../../features/login.feature"


# ── Scenario Declarations ─────────────────────────────────────
# Each @scenario binds a Python test function to a Gherkin scenario.

@scenario(FEATURE, "Successful login with valid credentials")
def test_successful_login():
    """pytest-bdd wires this to the Gherkin scenario."""


@scenario(FEATURE, "Failed login with wrong password")
def test_failed_login():
    pass


@scenario(FEATURE, "Empty form submission is rejected")
def test_empty_form():
    pass


# ── Background Steps (reused by every scenario) ───────────────

@given("the application is running")
def app_is_running(page: Page):
    """
    Background step 1 of 2.
    Navigate to the app and wait for it to fully load.
    'networkidle' waits until no network requests for 500ms —
    more reliable than arbitrary wall-clock sleeps in any environment.
    """
    page.goto(BASE_URL, wait_until="networkidle")


@given("I am on the login page")
def on_login_page(page: Page):
    """
    Background step 2 of 2.
    Assert we are on the login page before any scenario begins.
    This is a guard — if the app is misconfigured, this step
    fails loudly instead of producing a confusing later error.
    """
    expect(page).to_have_url(f"{BASE_URL}/login")
    expect(page.locator("h1")).to_have_text("Login")


# ── Scenario-Specific Steps ───────────────────────────────────

@when("I submit valid credentials")
def submit_valid_credentials(page: Page):
    page.fill("#username", "admin")
    page.fill("#password", "secret123")
    page.click("#login-btn")
    page.wait_for_load_state("networkidle")


@then("I should land on the dashboard")
def on_dashboard(page: Page):
    expect(page).to_have_url(f"{BASE_URL}/dashboard")
    expect(page.locator("h1")).to_have_text("Dashboard")


@when("I submit invalid credentials")
def submit_invalid_credentials(page: Page):
    page.fill("#username", "admin")
    page.fill("#password", "wrongpassword")
    page.click("#login-btn")


@then("I should see an error alert")
def see_error_alert(page: Page):
    error = page.locator("#error-msg")
    expect(error).to_be_visible()
    expect(error).to_contain_text("Invalid credentials")


@when("I submit an empty form")
def submit_empty_form(page: Page):
    # Click login without filling anything
    page.click("#login-btn")


@then("I should see a validation message")
def see_validation_message(page: Page):
    error = page.locator("#error-msg")
    expect(error).to_be_visible()
    expect(error).to_contain_text("required")
