# Lesson 10: Data Validator

## Overview
Production-grade CSV email validation system demonstrating:
- Path abstraction with pathlib
- Result objects with dataclasses
- Structured logging for CI/CD
- HTML report generation

## Quick Start
```bash
# Run the validator
python data_validator.py

# View HTML report
open validation_report.html  # macOS
xdg-open validation_report.html  # Linux
start validation_report.html  # Windows
```

## Architecture
- `CSVEmailValidator`: Core validation logic
- `DirectoryScanner`: File discovery and orchestration
- `ConsoleReporter`: Colored CLI output
- `HTMLReporter`: CI/CD artifact generation

## Success Criteria
✓ All empty email fields detected
✓ Exact row numbers reported
✓ HTML report generated
✓ Cross-platform compatibility
