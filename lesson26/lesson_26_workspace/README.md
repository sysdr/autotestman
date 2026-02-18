# Lesson 26: Screenshots on Failure

## Overview
This workspace demonstrates automatic screenshot capture on test failures using pytest hooks.

## Structure
```
lesson_26_workspace/
├── conftest.py              # Pytest hooks (the magic happens here)
├── pytest.ini               # Pytest configuration
├── tests/
│   └── test_demo.py         # Demo tests (2 pass, 2 fail intentionally)
├── utils/
│   └── screenshot_analyzer.py  # Utility to analyze screenshots
└── screenshots/             # Auto-generated screenshots organized by date
    └── YYYY-MM-DD/
        └── test_name_timestamp.png
```

## Quick Start

### 1. Install Dependencies
```bash
pip install selenium pytest pytest-html
```

### 2. Install ChromeDriver
- Download from: https://chromedriver.chromium.org/
- Or use: `pip install webdriver-manager`

### 3. Run Tests
```bash
pytest tests/ -v
```

### 4. Check Screenshots
```bash
ls -la screenshots/$(date +%Y-%m-%d)/
```

### 5. Generate HTML Report
```bash
python utils/screenshot_analyzer.py
open screenshots/report.html
```

## Expected Results
- `test_google_homepage_loads`: ✅ PASS (no screenshot)
- `test_google_search_functionality`: ✅ PASS (no screenshot)
- `test_intentional_failure_assertion`: ❌ FAIL (screenshot captured)
- `test_intentional_failure_missing_element`: ❌ FAIL (screenshot captured)

## Key Learning Points

1. **Zero Test Modification**: All 4 tests get screenshot capability without changing their code
2. **Unique Filenames**: Timestamps prevent race conditions in parallel execution
3. **Contextual Naming**: Filenames include test names for easy debugging
4. **Graceful Degradation**: Screenshot failures don't break test reporting

## Production Tips

- Enable parallel execution: `pytest tests/ -n 4` (requires pytest-xdist)
- CI/CD integration: Upload `screenshots/` as build artifacts
- Add browser name to filename for multi-browser testing
- Rotate old screenshots (e.g., delete files older than 7 days)

## The Engineering Lesson
This is **infrastructure as code**. One hook = automatic capability for all tests, forever.
