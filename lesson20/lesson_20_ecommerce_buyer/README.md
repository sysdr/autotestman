# Lesson 20: The E-Commerce Buyer

## Project Structure
```
lesson_20_ecommerce_buyer/
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── pages/                    # Page Object Model
│   ├── base_page.py         # Reusable wait mechanisms
│   ├── login_page.py        # Login functionality
│   ├── product_listing_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/                    # Test cases
│   └── test_ecommerce_flow.py
└── utils/                    # Utilities
    └── driver_factory.py    # WebDriver initialization
```

## Setup
```bash
pip install -r requirements.txt
```

## Run Tests

### With pytest (recommended):
```bash
pytest tests/test_ecommerce_flow.py -v -s
```

### Standalone:
```bash
python tests/test_ecommerce_flow.py
```

## What You'll Learn
- ✅ Explicit waits vs implicit waits
- ✅ Page Object Model pattern
- ✅ Custom expected conditions
- ✅ Production-ready test architecture
- ✅ Zero hard sleeps policy

## Success Metrics
- Test Stability: > 99%
- Execution Time: < 20s
- Zero `time.sleep()` usage
