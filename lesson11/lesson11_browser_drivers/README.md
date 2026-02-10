# Lesson 11: Browser Drivers & Navigation

## Quick Start

1. **Install dependencies:**
```bash
   pip install -r requirements.txt
```

2. **Run the test:**
```bash
   python tests/test_navigation.py
```

## What You'll See

The test runs twice:
1. **Headed mode**: Browser window opens visibly
2. **Headless mode**: Runs in background (CI/CD simulation)

## Success Criteria

✓ Both tests pass  
✓ Browser closes cleanly (no zombie processes)  
✓ Test completes in < 10 seconds  

## Troubleshooting

**ChromeDriver version mismatch:**
```bash
rm -rf ~/.wdm/
```

**Test hangs:**
- Check your internet connection
- Verify Chrome is installed

## Next Steps

Modify `pages/google_page.py` to add more interactions (search, click buttons, etc.)
