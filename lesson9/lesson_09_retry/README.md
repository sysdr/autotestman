# Lesson 9: Error Handling for Flakiness

## Setup Complete! ✅

Your workspace has been created with the following structure:
```
lesson_09_retry/
├── utils/
│   └── retry_decorator.py      # Core retry implementation
├── tests/
│   ├── test_retry_basic.py     # Basic functionality tests
│   └── test_retry_advanced.py  # Advanced scenario tests
└── demo/
    ├── flaky_api_simulator.py  # Simulated flaky services
    └── run_demo.py             # Interactive demonstration
```

## Quick Start

### 1. Run the Interactive Demo
```bash
cd lesson_09_retry
python demo/run_demo.py
```

### 2. Run the Test Suite
```bash
pytest tests/ -v --tb=short
```

### 3. Explore the Implementation
Open `utils/retry_decorator.py` to see the production-grade retry decorator.

## Key Concepts Demonstrated

1. **Python Decorators** - How to wrap functions with additional behavior
2. **Exponential Backoff** - Smart retry delays (1s, 2s, 4s...)
3. **Exception Filtering** - Only retry specific error types
4. **Metrics Tracking** - Monitor retry rates in production
5. **Type Hints** - Modern Python 3.11+ code practices

## Real-World Usage
```python
from utils.retry_decorator import retry

# Retry flaky API calls
@retry(attempts=3, delay=1, exceptions=(ConnectionError,))
def fetch_user_data(user_id):
    return requests.get(f"https://api.example.com/users/{user_id}")

# Retry browser interactions
@retry(attempts=3, exceptions=(StaleElementReferenceException,))
def click_button(driver):
    driver.find_element(By.ID, "submit").click()
```

## Production Checklist

- [ ] Tests pass with >99% success rate
- [ ] Retry rate < 5% in metrics
- [ ] Exponential backoff configured properly
- [ ] Assertion errors NOT being retried
- [ ] Logging enabled for CI/CD debugging
