# PyTest Fixtures Lesson

**Generated:** 2026-02-06 10:12:05

## Quick Start

1. Install dependencies:
```bash
   pip install pytest pytest-xdist
```

2. Run all tests:
```bash
   cd pytest_fixtures_lesson
   pytest tests/ -v
```

3. Run with cleanup verification:
```bash
   pytest tests/ -v && python -c "from utils.file_helpers import verify_cleanup; verify_cleanup()"
```

4. Run in parallel:
```bash
   pytest tests/ -n 4 -v
```

## Test Commands

- **Run single test:** `pytest tests/test_fixtures.py::test_with_temp_file -v`
- **Show fixture setup/teardown:** `pytest tests/ -v -s`
- **Run in random order:** `pytest tests/ --random-order`
- **Generate HTML report:** `pytest tests/ --html=report.html`

## Expected Output

You should see:
- ✅ All tests pass
- 🔧 SETUP/TEARDOWN messages for each fixture
- 🧹 No temp files remaining after test run

## Exercise

Modify `test_fixtures.py` to:
1. Create a fixture that sets up a CSV file with sample data
2. Use it in a test that parses the CSV
3. Verify cleanup happens even if parsing fails
