# Lesson 32: Async/Await & Locators

## Overview
This workspace demonstrates the difference between Selenium's explicit wait approach and Playwright's auto-waiting locators.

## Installation
```bash
pip install playwright pytest-playwright selenium --break-system-packages
playwright install chromium
```

## Running Tests

### Playwright (Recommended)
```bash
# Run with pytest
pytest tests/test_login_playwright.py -v

# Run standalone demo
python tests/test_login_playwright.py
```

### Selenium Comparison
```bash
python comparison/selenium_login.py
```

## Key Files
- `pages/login_page.py`: Page Object Model with auto-waiting locators
- `tests/test_login_playwright.py`: Async test implementation
- `utils/browser_factory.py`: Reusable browser configuration
- `comparison/selenium_login.py`: Old approach for comparison

## What You'll Learn
1. How async/await works in Python test automation
2. Why Playwright's locators are more stable than Selenium's
3. How to eliminate time.sleep() from your tests
4. The Page Object Model pattern with Playwright

## Success Criteria
- Test completes in < 5 seconds
- Zero explicit waits (no time.sleep())
- 99%+ stability across multiple runs
