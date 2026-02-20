# Lesson 29: Tagging & Grouping

## Quick Start

### 1. Install Dependencies
```bash
pip install pytest
```

### 2. Run Smoke Tests (Fast Feedback)
```bash
pytest -m smoke -v
```
**Expected:** ~6 tests, <2 seconds

### 3. Run Regression Tests (Comprehensive)
```bash
pytest -m regression -v
```
**Expected:** ~9 tests, slower execution

### 4. Run API Tests Only
```bash
pytest -m api -v
```

### 5. Complex Filtering
```bash
# Smoke tests that are also API tests
pytest -m "smoke and api" -v

# All tests except slow ones
pytest -m "not slow" -v

# Smoke OR regression (all tests)
pytest -m "smoke or regression" -v
```

## Workspace Structure

```
lesson_29_tagging/
├── pytest.ini                      # Marker definitions
├── conftest.py                     # Shared fixtures
├── tests/
│   ├── test_login.py              # Login tests (smoke + regression)
│   ├── test_checkout.py           # Checkout tests (mixed markers)
│   └── test_api.py                # Pure API tests
├── utils/
│   └── marker_statistics.py       # Analyze marker distribution
└── run_all_configurations.py      # Demo all marker combos
```

## Marker Definitions

- **smoke**: Critical path tests (must pass on every PR)
- **regression**: Edge case tests (run nightly)
- **api**: API endpoint tests
- **ui**: UI interaction tests
- **slow**: Tests >10 seconds
- **integration**: Multi-service tests
- **unit**: Isolated unit tests

## Running Utility Scripts

### All Configurations Demo
```bash
python run_all_configurations.py
```

### Marker Statistics
```bash
python utils/marker_statistics.py
```

## Expected Results

### Smoke Tests
- test_user_can_login_with_valid_credentials ✓
- test_login_api_returns_token ✓
- test_guest_checkout_completes ✓
- test_payment_api_processes_transaction ✓
- test_health_check_endpoint ✓
- test_user_profile_api ✓

**Total:** 6 tests, ~0.5-1 second

### Regression Tests
- test_login_fails_with_invalid_password ✓
- test_login_blocked_after_multiple_failures ✓
- test_login_with_expired_session ✓
- test_checkout_with_expired_coupon ✓
- test_checkout_with_insufficient_inventory ✓
- test_checkout_with_international_shipping ✓
- test_api_rate_limiting ✓
- test_api_with_large_payload ✓

**Total:** 8+ tests, 1-3 seconds

## CI/CD Integration

### GitHub Actions Example
```yaml
jobs:
  pr-checks:
    runs-on: ubuntu-latest
    steps:
      - run: pytest -m smoke --maxfail=1

  nightly:
    runs-on: ubuntu-latest
    if: github.event_name == 'schedule'
    steps:
      - run: pytest -m regression
```

## Troubleshooting

### Warning: Unknown Marker
```
PytestUnknownMarkWarning: Unknown pytest.mark.smoek
```
**Fix:** Check spelling in pytest.ini and test files.

### All Tests Run (No Filtering)
**Cause:** Typo in marker name or missing `-m` flag.
**Fix:** Verify with `pytest --markers` to see registered markers.

## Production Metrics

- **Smoke test duration:** <5 minutes (target: 2-3 min)
- **Marker coverage:** 100% of tests should have ≥1 marker
- **PR feedback time:** <5 minutes (smoke only)
- **Nightly build time:** <60 minutes (full regression)

## Next Steps

1. Add markers to your existing test suite
2. Configure CI/CD to run smoke on PRs
3. Schedule nightly regression runs
4. Monitor and optimize test execution times