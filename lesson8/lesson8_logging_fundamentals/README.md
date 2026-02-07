# Lesson 8: Logging Fundamentals

## Quick Start

1. **Run the comparison demo:**
   ```bash
   cd lesson8_logging_fundamentals
   python run_comparison.py
   ```

2. **Run verification tests:**
   ```bash
   python tests/test_logging_verification.py
   ```

3. **View the dashboard:**
   ```bash
   python serve_dashboard.py
   ```
   Then open: http://localhost:8000/logging_comparison.html

4. **Examine log files:**
   ```bash
   ls -lh logs/
   cat logs/session_*.log
   ```

## Files Overview

- `naive_print_approach.py` - Bad: Using print() statements
- `proper_logging_approach.py` - Good: Using logging module
- `utils/logging_config.py` - Reusable logging configuration
- `tests/test_logging_verification.py` - Verification tests
- `data/test_config.json` - Sample test data

## Key Concepts Demonstrated

1. **Log Levels:** DEBUG, INFO, WARNING, ERROR, CRITICAL
2. **Handlers:** Console vs File output with different formatting
3. **Formatters:** Structured log messages with metadata
4. **Logger Hierarchy:** Module-level loggers with inheritance
5. **Exception Logging:** Automatic traceback capture with logger.exception()

## Production Metrics

✓ All logs include timestamps (ISO 8601 format)
✓ Module and function names tracked automatically
✓ Console output filtered by severity (INFO+)
✓ Complete debug logs written to file
✓ Exit codes properly set for CI/CD integration
