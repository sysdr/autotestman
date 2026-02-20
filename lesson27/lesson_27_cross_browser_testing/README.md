# Lesson 27: Chrome Testing

## Overview
Chrome testing framework using Pytest and the Factory Pattern with automatic ChromeDriver management.

## Architecture
- **Browser Factory**: Centralized Chrome WebDriver creation
- **Page Objects**: Browser-agnostic page interactions
- **Pytest Fixtures**: Single browser (Chrome) fixture
- **Automatic Driver Management**: No manual driver downloads

## Setup

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Tests

#### Chrome
```bash
pytest tests/ -v
```

#### With Browser Flag
```bash
pytest tests/ --browser=chrome -v
```

#### Slow Mode (watch each step)
```bash
pytest tests/ --slow 1.5 -v
```
Use `--slow` with seconds (e.g. `1.5` or `2`) to pause after each action so you can see what the test is doing.

#### Headless Mode
```bash
pytest tests/ --headless -v
```

#### Parallel Execution
```bash
pytest tests/ -n 3 -v
```

#### With HTML Report
```bash
pytest tests/ --html=reports/report.html --self-contained-html
```

## Project Structure
```
lesson_27_cross_browser_testing/
├── config/
│   └── test_config.py          # Centralized configuration
├── pages/
│   └── login_page.py            # Page Object Model
├── tests/
│   ├── conftest.py              # Pytest fixtures
│   └── test_cross_browser.py    # Test suite
├── utils/
│   └── browser_factory.py       # Browser creation factory
├── reports/                     # Test reports and screenshots
└── requirements.txt
```

## Key Concepts

### Factory Pattern
Single source of truth for creating browser instances:
```python
driver = BrowserFactory.create_driver("chrome")
```

### Pytest Fixture
Chrome browser fixture:
```python
@pytest.fixture(params=["chrome"])
def browser(request):
    ...
```

### Tests
Test code uses the browser fixture:
```python
def test_login(browser):
    browser.get("https://example.com")
    ...
```

## Success Metrics
✅ Code Reusability: 100% (zero duplication)
✅ Test Stability: >99% pass rate
✅ Execution Efficiency: Parallel execution support
✅ Maintainability: Chrome-only, minimal setup

## Troubleshooting

### Driver Download Issues
If webdriver-manager fails, clear the cache:
```bash
rm -rf ~/.wdm
```

### Chrome Not Installed
Install Chrome: https://www.google.com/chrome/

### Tests Fail
Check Chrome version compatibility. Webdriver-manager should auto-update ChromeDriver.

## Next Steps
- Lesson 28: Parallel Test Execution
- Lesson 29: Docker-based Test Execution
- Lesson 30: CI/CD Integration
