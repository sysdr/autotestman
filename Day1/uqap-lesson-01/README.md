# UQAP Lesson 1: Environment Setup

## Overview
This project demonstrates production-grade Python test automation environment setup.

## Quick Start

### 1. Create Virtual Environment
```bash
python -m venv .venv
```

### 2. Activate Virtual Environment
**macOS/Linux:**
```bash
source .venv/bin/activate
```

**Windows (Command Prompt):**
```bash
.venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```bash
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -e .
```

### 4. Run Hello Automation
```bash
python src/automation/hello.py
```

### 5. Run Tests
```bash
pytest tests/ -v
```

## Project Structure
```
uqap-lesson-01/
├── src/
│   └── automation/
│       ├── __init__.py
│       └── hello.py          # Main automation script
├── tests/
│   ├── __init__.py
│   └── test_hello.py         # Test suite
├── pyproject.toml            # Project dependencies
├── .gitignore
└── README.md
```

## Verification Checklist
- [ ] Python 3.11+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] `hello.py` runs without errors
- [ ] All tests pass

## Next Steps
Lesson 2: File manipulation and CSV parsing for test data management.
