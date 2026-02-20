# Lesson 31: Playwright Setup & Codegen

## Quick Start

### 1. Install Dependencies
```bash
pip install playwright pytest pytest-asyncio pytest-playwright
playwright install chromium
```

### 2. Run Tests
```bash
# Run all tests (headless)
pytest tests/ -v

# Run with visible browser
pytest tests/ -v --headed

# Run specific test class
pytest tests/test_todo.py::TestTodoBasicOperations -v

# Run with live output
pytest tests/ -v -s
```

### 3. Generate Code with Playwright Codegen
```bash
# Open codegen tool
playwright codegen https://demo.playwright.dev/todomvc

# Record your actions, then copy the generated code
# Compare with codegen_output/raw_codegen_example.py
```

## Project Structure
```
playwright_lesson_31/
├── config/
│   └── config.py          # Configuration management
├── pages/
│   ├── base_page.py       # Base page class
│   └── todo_page.py       # TodoMVC page object
├── tests/
│   └── test_todo.py       # Test suite
├── utils/
│   └── helpers.py         # Utility functions
├── codegen_output/
│   └── raw_codegen_example.py  # Raw codegen for comparison
├── conftest.py            # Pytest fixtures
└── pytest.ini             # Pytest configuration
```

## Key Concepts Demonstrated

### 1. Codegen as Starting Point
- Use `playwright codegen` to explore application
- Extract patterns from generated code
- Refactor into Page Object Model

### 2. Page Object Model
- Centralize locators in page classes
- Create reusable action methods
- Add assertions to verify state

### 3. Pytest Integration
- Async fixtures for browser/page management
- Automatic screenshot on failure
- Test isolation with function-scoped contexts

### 4. Configuration Management
- Environment-driven configuration
- Support for multiple environments
- CI/CD specific settings

## Common Commands

```bash
# Run smoke tests only
pytest tests/ -v -m smoke

# Run with HTML report
pytest tests/ --html=report.html --self-contained-html

# Run 10 times to check stability
pytest tests/test_todo.py --count=10

# Run with coverage
pytest tests/ --cov=pages --cov=utils --cov-report=html

# Debug mode (stop on first failure)
pytest tests/ -x --pdb
```

## Next Steps

1. Add more test scenarios
2. Integrate with CI/CD (GitHub Actions, GitLab CI)
3. Add parallel execution (pytest-xdist)
4. Add visual regression testing
5. Add API test integration

## Production Checklist

- [ ] Tests pass 100/100 times locally
- [ ] Execution time < 5s per test
- [ ] Screenshots on failure enabled
- [ ] Traces enabled for debugging
- [ ] Config externalized (environment variables)
- [ ] CI/CD pipeline configured
- [ ] Monitoring/alerting setup
