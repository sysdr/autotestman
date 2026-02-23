# Lesson 34: API Interception (Network Mocking)

## Overview
Learn to test error handling by intercepting network requests and mocking API responses.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt --break-system-packages
playwright install chromium
```

2. Start the web server (Terminal 1):
```bash
python app/server.py
```

3. Run tests (Terminal 2):
```bash
pytest tests/test_api_error_handling.py -v
```

## What You'll Learn

- Intercept HTTP requests at the browser level
- Mock API error responses (500, 404, 401)
- Simulate network failures
- Test UI error handling deterministically
- Build production-ready error handling tests

## Project Structure

```
lesson_34_api_interception/
├── tests/
│   └── test_api_error_handling.py    # Test suite
├── app/
│   ├── index.html                     # Dashboard UI
│   └── server.py                      # Local HTTP server
├── pages/
│   └── dashboard_page.py              # Page Object Model
└── utils/
    └── network_mock.py                # Interception utilities
```

## Running Tests

### Run all tests:
```bash
pytest tests/ -v
```

### Run with visible browser:
```bash
pytest tests/ --headed
```

### Run specific test:
```bash
pytest tests/test_api_error_handling.py::TestAPIErrorHandling::test_500_server_error_shows_message -v
```

## Key Concepts

1. **Network Interception**: Control HTTP requests before they reach the network
2. **Deterministic Testing**: Same input = same output, every time
3. **Error Coverage**: Test all error scenarios (5xx, 4xx, network failures)
4. **Fast Feedback**: Tests run at CPU speed, not network speed

## Production Metrics

- Test Stability: > 99% pass rate
- Execution Time: < 2s per scenario
- Zero Dependencies: No backend services required
