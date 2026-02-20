# Lesson 30: Framework Review

## Quick Start

1. **Review the Before/After code:**
```bash
   # Compare untyped vs typed code
   diff framework_before/base_page.py framework_after/base_page.py
```

2. **Run type checking:**
```bash
   # Check the 'after' version (should pass)
   mypy framework_after/base_page.py
   
   # Try checking the 'before' version (will fail)
   mypy framework_before/base_page.py
```

3. **Run verification tests:**
```bash
   python tests/test_framework.py
```

4. **View the comparison report:**
```bash
   # Open in browser
   open reports/comparison.html
   # or
   xdg-open reports/comparison.html
```

## What You'll Learn

- Adding type hints to existing code
- Writing Google-style docstrings
- Using mypy for static type checking
- Measuring code quality metrics

## Success Criteria

✓ Type hint coverage: 100%
✓ Docstring coverage: 100%  
✓ mypy --strict passes with 0 errors
✓ All tests pass
