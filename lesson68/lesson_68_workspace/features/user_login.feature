Feature: User Authentication
  As a registered user
  I want to log in to the platform
  So that I can access my personalised dashboard

  Background:
    Given the authentication service is running

  Scenario: Successful login with valid credentials
    Given I have a valid account with username "alice" and password "Secure@123"
    When I submit the login form with username "alice" and password "Secure@123"
    Then I should be redirected to the dashboard
    And the welcome banner should display "Welcome, alice"

  Scenario: Failed login with wrong password
    Given I have a valid account with username "alice" and password "Secure@123"
    When I submit the login form with username "alice" and password "WrongPass"
    Then I should see the error "Invalid credentials. Please try again."

  Scenario: Login blocked after 3 failed attempts
    Given I have a valid account with username "bob" and password "Pass@456"
    When I fail to login 3 times with username "bob"
    Then the account should be temporarily locked
    And I should see the error "Account locked. Try again in 15 minutes."

  Scenario: Login with empty password field
    Given the login form is visible
    When I submit the login form with username "alice" and password ""
    Then I should see the error "Password is required."
