# Lesson 16: Alert Handling

    ## Quick Start
```bash
    # Install dependencies
    pip install selenium pytest webdriver-manager

    # Run tests
    cd lesson_16_alerts
    pytest tests/test_alerts.py -v
```

    ## What's Included

    - `demo.html`: Interactive demo page with various alert types
    - `utils/alert_handler.py`: Production-grade AlertHandler class
    - `pages/alert_page.py`: Page Object Model for the demo
    - `tests/test_alerts.py`: Comprehensive test suite

    ## Key Concepts

    1. **No time.sleep()**: All waits use explicit WebDriverWait
    2. **Context Managers**: Guaranteed cleanup with __enter__/__exit__
    3. **Type Hints**: Full typing for IDE support
    4. **Logging**: Comprehensive logging for debugging

    ## Running Specific Tests
```bash
    # Run single test
    pytest tests/test_alerts.py::test_js_alert_accept -v

    # Run with coverage
    pytest tests/test_alerts.py --cov=utils --cov=pages

    # Run 100 times to check stability
    pytest tests/test_alerts.py --count=100
```