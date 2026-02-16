# Lesson 19: Action Chains (Drag & Drop)

    ## Quick Start
```bash
    # Install dependencies
    pip install -r requirements.txt

    # Run test
    pytest tests/test_kanban_drag.py -v

    # Run in headless mode (CI simulation)
    pytest tests/test_kanban_drag.py --headless -v

    # Run 10 times to verify stability
    pytest tests/test_kanban_drag.py --count=10
```

    ## What You'll Learn

    - Breaking drag-and-drop into atomic ActionChain steps
    - Implementing retry logic with exponential backoff
    - Using JavaScript for DOM verification (not visual)
    - Handling iframe contexts in web automation

    ## Production Metrics

    - **Stability Target**: >99% (1 failure per 100 runs)
    - **Execution Time**: <10s per test
    - **CI/CD Ready**: Zero manual intervention required

    ## Troubleshooting

    **Test fails with MoveTargetOutOfBoundsException:**
    - Ensure ChromeDriver version matches Chrome
    - Try increasing pause durations in `drag_drop_helper.py`

    **Test times out:**
    - Check internet connection (demo site is external)
    - Verify iframe switching is working (`driver.switch_to.frame()`)