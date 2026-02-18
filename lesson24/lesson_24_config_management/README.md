# Lesson 24: Managing Configuration

## Quick Start

1. **Install dependencies:**
```bash
pip install selenium pytest
```

2. **Run verification:**
```bash
python framework/verify_config.py
```

3. **Run tests in UI mode:**
```bash
# Edit config/config.ini and set: headless = false
python -m pytest tests/ -v -s
```

4. **Run tests in headless mode:**
```bash
# Edit config/config.ini and set: headless = true
python -m pytest tests/ -v -s
```

5. **Override with environment variable:**
```bash
export HEADLESS=true
python -m pytest tests/ -v -s
```

## Key Files

- `config/config.ini` - All configuration settings
- `framework/config_manager.py` - Singleton config loader
- `framework/driver_factory.py` - WebDriver factory
- `tests/test_config_demo.py` - Demonstration tests

## Learning Objectives

✓ Separate configuration from code
✓ Implement Singleton pattern in Python
✓ Support environment variable overrides
✓ Build production-ready test infrastructure
