# Lesson 3: Production-Grade JSON Parsing

## Overview
This lesson demonstrates defensive JSON parsing patterns used in production test infrastructure.

## Key Concepts
- Schema validation with dataclasses
- Error boundaries and safe parsing
- Type coercion and default values
- Logging for production debugging

## Quick Start
```bash
# Run the test suite
python tests/test_user_parser.py

# View results
open output/report.html  # macOS
xdg-open output/report.html  # Linux
start output/report.html  # Windows
```

## What You'll Learn

1. **Why naive JSON parsing fails in CI/CD**
2. **Defensive programming patterns**
3. **Schema validation without heavy frameworks**
4. """**Error handling that doesn't crash pipelines** """

## Project Structure
```
lesson_03_json_parsing/
├── data/
│   └── users.json          # Sample data with edge cases
├── utils/
│   ├── user_model.py       # Dataclass with safe parsing
│   └── parser.py           # JSON parsing utilities
├── tests/
│   └── test_user_parser.py # Test suite
└── output/
    └── report.html         # Generated visualization
```

## Expected Output

The test should:
- Parse 10+ users from JSON (with some records failing gracefully)
- Filter for adults (age > 18)
- Generate an HTML report
- Show 100% test pass rate despite malformed input data

## Production Metrics

- **Parse Success Rate**: Should be > 95%
- **Zero Crashes**: Malformed data never crashes the pipeline
- **Audit Trail**: All parsing failures are logged
