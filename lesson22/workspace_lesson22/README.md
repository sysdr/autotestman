# Lesson 22: Abstracting the Base Page

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run tests:
```bash
pytest tests/test_base_page.py -v
```

## What You'll Learn

- How to create a reusable BasePage class
- Why explicit waits beat time.sleep()
- How inheritance eliminates code duplication
- Production-ready error handling

## File Structure
```
workspace_lesson22/
├── core/
│   └── base_page.py       # The foundation: generic methods
├── pages/
│   ├── login_page.py      # Inherits BasePage
│   ├── dashboard_page.py  # Inherits BasePage
│   └── profile_page.py    # Inherits BasePage
├── tests/
│   └── test_base_page.py  # Demonstrates the pattern
└── requirements.txt
```

## Key Takeaways

- **Zero Duplication:** All pages use same click/type/find logic
- **Consistent Waits:** Explicit waits (not sleep) everywhere
- **Easy Maintenance:** Change BasePage once, all pages benefit
- **Production Ready:** Built-in logging and screenshots
