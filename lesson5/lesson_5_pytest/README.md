# Lesson 5: Introduction to PyTest

## Setup

1. Install dependencies:
```bash
   pip install -r requirements.txt --break-system-packages
```

2. Verify installation:
```bash
   pytest --version
```

## Running Tests

### Run all tests:
```bash
pytest -v
```

### Run specific test file:
```bash
pytest tests/test_data_validation.py -v
```

### Run specific test:
```bash
pytest tests/test_data_validation.py::test_user_emails_are_valid -v
```

### Show fixture setup/teardown:
```bash
pytest --setup-show
```

### Run tests in random order (verify isolation):
```bash
pytest --random-order
```

### Run tests matching a pattern:
```bash
pytest -k "email" -v
```

## Expected Output

All tests should pass:
- 4 tests in test_data_validation.py
- 3 tests in test_file_operations.py
- Total: 7 tests

## Verification

Run this command to verify everything works:
```bash
pytest -v --tb=short
```

You should see:
```
tests/test_data_validation.py::test_user_emails_are_valid PASSED
tests/test_data_validation.py::test_user_ids_are_unique PASSED
tests/test_data_validation.py::test_config_has_required_fields PASSED
tests/test_data_validation.py::test_active_users_count PASSED
tests/test_file_operations.py::test_create_and_read_file PASSED
tests/test_file_operations.py::test_workspace_isolation PASSED
tests/test_file_operations.py::test_multiple_files_in_workspace PASSED

========================= 7 passed in 0.XX s =========================
```
