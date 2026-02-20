# Lesson 28: Parallel Execution Demo

## Overview
This workspace demonstrates parallel test execution using pytest-xdist.
We have 12 tests across 3 test files, each taking ~1.5 seconds.

## Test Structure
```
tests/
├── test_api.py          # 4 API endpoint tests
├── test_database.py     # 4 database operation tests
└── test_integration.py  # 4 integration workflow tests
```

## Running Tests

### Sequential Execution (Baseline)
```bash
pytest tests/ -v
# Expected time: ~18 seconds (12 tests × 1.5s each)
```

### Parallel Execution (4 Workers)
```bash
pytest tests/ -n 4 -v
# Expected time: ~4.5 seconds (3× speedup)
```

### Parallel Execution (Auto-detect cores)
```bash
pytest tests/ -n auto -v
```

### See Worker Distribution
```bash
pytest tests/ -n 4 -v | grep -E "\[gw[0-9]\]"
```

## Key Concepts Demonstrated

1. **Worker Isolation**: Each worker has its own database, port, and temp directory
2. **Load Balancing**: Tests are distributed evenly across workers
3. **Fixture Scoping**: Session-scoped fixtures are created per worker
4. **No Shared State**: Workers don't interfere with each other

## Verification

Run the verification script:
```bash
python ../verify_speedup.py
```

This will measure sequential vs. parallel execution and calculate speedup.
