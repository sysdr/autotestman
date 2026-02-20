"""
RAW CODEGEN OUTPUT - DO NOT USE IN PRODUCTION
This is what Playwright codegen generates automatically.
Compare with the refactored version in pages/todo_page.py
"""
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    # PROBLEM 1: Hardcoded URL (should be configurable)
    page.goto("https://demo.playwright.dev/todomvc/")
    
    # PROBLEM 2: No proper wait (relies on auto-wait only)
    page.get_by_placeholder("What needs to be done?").click()
    
    # PROBLEM 3: No abstraction (action tied to implementation)
    page.get_by_placeholder("What needs to be done?").fill("Buy groceries")
    page.get_by_placeholder("What needs to be done?").press("Enter")
    
    # PROBLEM 4: No assertions (just performs actions)
    page.get_by_placeholder("What needs to be done?").fill("Walk the dog")
    page.get_by_placeholder("What needs to be done?").press("Enter")
    
    # PROBLEM 5: Selector may break (text-based, fragile)
    page.locator("li").filter(has_text="Buy groceries").get_by_label("Toggle Todo").check()
    
    # PROBLEM 6: No cleanup, no error handling
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)


"""
ANALYSIS OF PROBLEMS:

1. HARDCODED URL:
   - Fails when testing different environments (dev/staging/prod)
   - Solution: Config-driven base_url

2. NO PROPER WAITS:
   - Relies on Playwright's auto-wait (30s default)
   - Fails on slow networks in CI/CD
   - Solution: Explicit wait_for_element() calls

3. NO ABSTRACTION:
   - Every test repeats the same locators
   - One UI change breaks 100 tests
   - Solution: Page Object Model

4. NO ASSERTIONS:
   - Test "passes" even if functionality broken
   - Silent failures in CI/CD
   - Solution: expect() assertions after each action

5. FRAGILE SELECTORS:
   - Text changes break tests (internationalization)
   - Layout changes break positional selectors
   - Solution: data-testid attributes or role-based selectors

6. NO ERROR HANDLING:
   - No screenshots on failure
   - No trace collection for debugging
   - Solution: pytest fixtures with automatic cleanup

REFACTORING STRATEGY:
1. Extract locators → Put in TodoPage class
2. Add waits → Implement in BasePage
3. Add assertions → Use Playwright's expect()
4. Add config → Create config.py
5. Add fixtures → Use conftest.py
6. Add error handling → pytest hooks + screenshots
"""
