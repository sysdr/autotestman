
    # Lesson 15: Handling Dropdowns & Selects

    ## Overview
    This lesson demonstrates production-grade dropdown handling for both native `<select>` elements
    and custom div-based dropdowns commonly used in modern web frameworks.

    ## Structure
```
    lesson_15_dropdowns/
    ├── tests/
    │   └── test_dropdowns.py          # Test cases
    ├── pages/
    │   └── dropdown_page.py           # Page Object Model
    ├── utils/
    │   ├── dropdown_handler.py        # Core dropdown logic
    │   └── wait_conditions.py         # Custom wait conditions
    └── fixtures/
        └── test_page.html             # Test HTML page
```

    ## Running Tests

    1. Install dependencies:
```bash
       pip install selenium pytest webdriver-manager
```

    2. Run tests:
```bash
       python -m pytest tests/test_dropdowns.py -v
```

    ## Key Concepts

    - **Explicit Waits**: Replace time.sleep() with intelligent polling
    - **Strategy Pattern**: Different handlers for different dropdown types
    - **Verification Loop**: Always verify selections persisted
    - **Page Object Model**: Separate test logic from implementation details

    ## Performance Targets

    - Test stability: > 99%
    - Execution time: < 2s per interaction
    - No flaky tests due to timing issues
