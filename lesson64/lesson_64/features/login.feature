Feature: User Authentication
  As a registered user
  I want to log in to the application
  So that I can access my dashboard

  # ─────────────────────────────────────────────────────
  # Background runs BEFORE EVERY scenario in this file.
  # This is where business prerequisites live.
  # PMs and BAs can read and validate these lines.
  # ─────────────────────────────────────────────────────
  Background:
    Given the application is running
    And I am on the login page

  Scenario: Successful login with valid credentials
    When I submit valid credentials
    Then I should land on the dashboard

  Scenario: Failed login with wrong password
    When I submit invalid credentials
    Then I should see an error alert

  Scenario: Empty form submission is rejected
    When I submit an empty form
    Then I should see a validation message
