
    # Visual Regression Testing - Lesson 35

    ## Overview
    Production-grade visual regression testing using Playwright and pixel-perfect comparison.

    ## Installation
```bash
    pip install -r requirements.txt
    playwright install chromium
```

    ## Usage

    ### First Run (Creates Baselines)
```bash
    pytest tests/ -v
```

    Expected output:
```
    test_homepage_visual PASSED - Baseline created
    test_responsive_mobile_visual PASSED - Baseline created
```

    ### Subsequent Runs (Compares Against Baselines)
```bash
    pytest tests/ -v
```

    Expected output:
```
    test_homepage_visual PASSED - Visual regression check passed (0.02% diff)
    test_responsive_mobile_visual PASSED - Visual regression check passed (0.03% diff)
```

    ## Directory Structure
```
    visual_regression_test/
    ├── tests/                    # Test files
    │   └── test_visual_regression.py
    ├── utils/                    # Utility modules
    │   └── visual_comparator.py
    ├── baselines/                # Golden baseline screenshots
    │   ├── homepage.png
    │   └── homepage_mobile.png
    ├── screenshots/              # Current test screenshots
    │   ├── homepage.png
    │   └── homepage_mobile.png
    └── diffs/                    # Visual diff images (only on failures)
        └── homepage_diff.png
```

    ## Simulating a Failure

    To see the diff generation in action:

    1. Run tests once to create baselines
    2. Edit `test_visual_regression.py` and change viewport dimensions:
```python
       page = browser.new_page(viewport={"width": 1920, "height": 1080})  # Changed from 1280x720
```
    3. Run tests again
    4. Check `diffs/homepage_diff.png` to see highlighted changes

    ## Key Features

    - **Baseline Management:** First run creates golden screenshots
    - **Pixel Tolerance:** 0.1% threshold handles anti-aliasing drift
    - **Diff Generation:** Visual highlighting of changed regions
    - **Multi-Viewport:** Test responsive designs across different screen sizes
    - **Production-Ready:** Clean architecture, type hints, comprehensive error handling

    ## Threshold Configuration

    Adjust tolerance in the `visual_regression` fixture:
```python
    return VisualRegression(baseline_dir=baseline_dir, threshold=0.5)  # Allow 0.5% difference
```

    ## Updating Baselines

    When UI changes are intentional:
```bash
    # Delete old baselines
    rm baselines/*.png

    # Run tests to create new baselines
    pytest tests/ -v
```
