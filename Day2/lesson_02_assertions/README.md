# Lesson 2: Deep Dictionary Comparison

A production-grade dictionary comparison utility with custom assertions, comprehensive error reporting, and HTML dashboard visualization.

## Overview

This lesson demonstrates how to build robust dictionary comparison logic for test automation. Instead of using simple `assert dict1 == dict2`, this implementation provides:

- **Deep recursive comparison** of nested dictionaries and lists
- **Comprehensive difference collection** (not just the first mismatch)
- **Path breadcrumbs** for easy debugging of nested structures
- **Exclusion rules** for dynamic fields (timestamps, IDs, etc.)
- **Rich diagnostic reports** with custom exceptions
- **HTML dashboard** for test results visualization

## Project Structure

```
lesson_02_assertions/
├── utils/
│   └── comparator.py      # DictComparator class and utilities
├── tests/
│   └── test_comparator.py # Pytest test suite
├── output/
│   └── comparison_report.html  # HTML dashboard
├── setup.py               # Interactive demo and report generator
├── cleanup.sh             # Docker and cache cleanup script
├── .gitignore             # Git ignore patterns
└── README.md
```

## Setup

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Install dependencies
pip install pytest
```

## Usage

### Run Tests

```bash
# From lesson_02_assertions directory
pytest tests/test_comparator.py -v
```

### Run Interactive Demo

```bash
# From lesson_02_assertions directory
python setup.py
```

This will:
- Run all test scenarios interactively
- Generate the HTML dashboard report
- Display summary statistics

### View Dashboard

After running `setup.py`, view the HTML dashboard:

```bash
# Option 1: Open directly in browser
# File location: output/comparison_report.html

# Option 2: Serve via HTTP (from lesson_02_assertions directory)
cd output
python3 -m http.server 8000
# Then open: http://localhost:8000/comparison_report.html
```

## Features

### 1. Deep Dictionary Comparison

```python
from utils.comparator import DictComparator

comparator = DictComparator()
comparator.assert_equal(expected_dict, actual_dict)
```

### 2. Exclusion Rules

Ignore dynamic fields like timestamps and request IDs:

```python
comparator = DictComparator(exclude_keys={"timestamp", "request_id"})
comparator.assert_equal(expected, actual)
```

### 3. Custom Exception with Diagnostics

```python
from utils.comparator import DictMismatchError

try:
    comparator.assert_equal(expected, actual)
except DictMismatchError as e:
    print(e)  # Rich diagnostic report with all differences
```

## Test Cases

The test suite includes:

1. **test_identical_dicts** - Verifies identical dictionaries pass
2. **test_value_mismatch** - Catches value mismatches
3. **test_nested_mismatch** - Handles nested structure comparison
4. **test_exclude_keys** - Tests exclusion of dynamic keys
5. **test_missing_keys** - Detects missing required keys
6. **test_list_comparison** - Compares list elements
7. **test_email_mismatch_sample** - Sample failure scenario

## Key Learnings

1. **Never use `assert dict1 == dict2` in production** - Provides no diagnostic information
2. **Always collect ALL differences** - Don't stop at the first mismatch
3. **Maintain path breadcrumbs** - Essential for debugging nested structures
4. **Allow exclusion rules** - Handle dynamic fields gracefully
5. **Raise custom exceptions** - Provide rich diagnostics for faster debugging

## Dashboard Features

The HTML dashboard (`output/comparison_report.html`) provides:

- ✅ Test summary with pass/fail counts
- 📊 Success rate metrics
- 📎 Sample failure demonstrations
- ⏱ Performance metrics
- 🎨 Modern, responsive design

## Cleanup

To clean up Docker resources and cache files:

```bash
# From lesson_02_assertions directory
./cleanup.sh
```

This removes:
- Docker containers, images, volumes
- Python cache files (__pycache__, *.pyc)
- pytest cache
- node_modules
- Virtual environments
- Istio files

## Contributing

When adding new test cases:
1. Add test function to `tests/test_comparator.py`
2. Follow naming convention: `test_<feature_name>`
3. Run `pytest tests/test_comparator.py -v` to verify
4. Regenerate dashboard: `python setup.py`
