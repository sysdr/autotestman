# UQAP Lesson 4: Data Parsing

Production-grade CSV/Excel parsing for test automation.

## Quick Start
```bash
# Install dependencies
pip install pandas openpyxl pytest

# Run the parser
python src/data_parser.py

# Run tests
pytest tests/ -v
```

## Project Structure
```
uqap-lesson-04/
├── src/
│   ├── models.py          # TestUser dataclass
│   └── data_parser.py     # CSV/Excel loaders
├── tests/
│   └── test_data_parser.py
├── data/
│   └── test_users.csv     # Sample test data
└── pyproject.toml
```

## Key Concepts

1. **Type Safety**: Dataclasses with validation
2. **Format Agnostic**: CSV and Excel support
3. **Memory Efficient**: Iterator pattern for large files
4. **Production Ready**: Encoding handling, error messages

## Next Steps

See main course for integration with pytest parameterization.
