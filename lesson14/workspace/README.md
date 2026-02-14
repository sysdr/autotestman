# Lesson 12: Locator Strategy (CSS vs. XPath)

## Overview

This workspace demonstrates production-grade locator strategies for Selenium WebDriver testing.

## Quick Start

### 1. Install Dependencies
```bash
pip install selenium pytest pytest-html
```

### 2. Run Tests
```bash
cd workspace
pytest tests/test_locator_strategy.py -v
```

### 3. Generate HTML Report
```bash
pytest tests/test_locator_strategy.py --html=reports/locator_comparison.html --self-contained-html
```

### 4. Run Visual Demo (Browser Visible)
```bash
python -c "from tests.test_locator_strategy import test_visual_demo; test_visual_demo()"
```

## Project Structure
```
workspace/
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures
│   └── test_locator_strategy.py  # Main test suite
├── pages/
│   ├── __init__.py
│   └── demo_page.py              # Page Object Model
├── utils/
│   ├── __init__.py
│   └── metrics.py                # Performance measurement
├── html/
│   └── test_page.html            # Demo page for testing
└── reports/
    └── locator_comparison.html   # Generated report
```

## Key Concepts

### Locator Hierarchy (Best to Worst)

1. **ID** - Fastest, most stable
2. **CSS Selector** - Fast, flexible, recommended
3. **XPath** - Powerful but slow, use only when necessary

### When to Use Each

- **ID**: Always use if available
- **CSS**: 90% of cases
- **XPath**: Only for text content or upward traversal

### Anti-Patterns to Avoid

❌ Absolute XPath: `/html/body/div[1]/div[2]/button`
❌ Generic classes without context
❌ Copy-paste from browser DevTools

## Success Metrics

- ✅ Test stability > 99%
- ✅ CSS execution < 50ms
- ✅ Survives HTML refactoring

## Next Steps

1. Review the generated HTML report
2. Experiment with different locator strategies
3. Practice refactoring fragile locators
4. Move on to Lesson 13: Explicit Waits
