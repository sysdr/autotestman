# Lesson 21: Page Object Model (POM) Implementation

## Overview
This workspace demonstrates a production-grade Page Object Model implementation for login automation using Selenium and pytest.

## Structure
```
lesson_21_pom_workspace/
├── pages/
│   ├── base_page.py          # Foundation class with common methods
│   ├── login_page.py         # Login page object
│   └── products_page.py      # Products page object
├── tests/
│   ├── conftest.py           # Pytest fixtures
│   └── test_login.py         # Login test suite
├── utils/
│   └── driver_manager.py     # WebDriver configuration
└── requirements.txt          # Dependencies

```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run all tests:
```bash
pytest tests/test_login.py -v
```

3. Run specific test:
```bash
pytest tests/test_login.py::TestLogin::test_successful_login_standard_user -v
```

4. Run with HTML report:
```bash
pytest tests/test_login.py --html=reports/report.html --self-contained-html
```

## Key Features

- ✅ **Explicit Waits**: No time.sleep() calls
- ✅ **DRY Principle**: Locators defined once in page objects
- ✅ **Type Hints**: Full IDE autocomplete support
- ✅ **Fluent API**: Method chaining for readable tests
- ✅ **Separation of Concerns**: Tests contain only business logic

## Test Coverage

- Successful login with valid credentials
- Login failures (invalid username, password, locked user)
- Empty credential handling
- Fluent API demonstration

## Extending This Framework

To add a new page:

1. Create `pages/new_page.py`
2. Inherit from `BasePage`
3. Define locators as class constants
4. Implement page-specific methods
5. Return next page objects from navigation methods

## Troubleshooting

**ChromeDriver issues:**
- webdriver-manager auto-downloads correct version
- If fails, manually specify chromedriver path

**Flaky tests:**
- Check for time.sleep() usage (should be zero)
- Verify explicit waits are used
- Increase timeout in BasePage if needed

**Element not found:**
- Verify locators match current website
- Check if page loaded completely
- Use driver_visible fixture for debugging
