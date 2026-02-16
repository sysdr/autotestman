# Lesson 18: Window Handling

Automated browser testing for multi-window and multi-tab scenarios using Selenium WebDriver and Python. This project demonstrates production-grade window/tab handling with explicit waits, automatic cleanup, and the Page Object Model.

## What It Does

- Opens new browser tabs or windows from a demo page
- Switches to the new window using explicit waits (no fixed sleeps)
- Verifies URL and content
- Closes the new window and restores focus to the original
- Ensures cleanup even when tests fail (context manager pattern)

## Prerequisites

- Python 3.10+
- Chrome browser
- ChromeDriver (installed automatically via `webdriver-manager`)

## Project Structure

```
lesson18_window_handling/
├── tests/
│   ├── conftest.py          # Pytest fixtures (browser, demo URL, window-leak check)
│   └── test_window_handling.py
├── pages/
│   └── demo_page.py         # Page Object for the demo HTML page
├── utils/
│   ├── window_manager.py   # Context manager for window/tab handling
│   └── visualizer.py       # Execution flow visualization (educational)
├── reports/                # Test reports (optional)
├── demo_page.html          # Main demo page
├── new-tab.html            # Page opened in new tab
├── new-window.html         # Page opened in new window
├── requirements.txt
├── pytest.ini
├── cleanup.sh              # Docker cleanup script
├── .gitignore
└── README.md
```

## Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/macOS
   # or: venv\Scripts\activate   # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Running Tests

From the `lesson18_window_handling` directory:

```bash
pytest tests/test_window_handling.py -v
```

Tests run in headless Chrome by default. To see the browser window, set:

```bash
HEADED=1 pytest tests/test_window_handling.py -v
```

## Execution Flow Visualizer

To see a step-by-step explanation of how the window manager works (no browser):

```bash
python utils/visualizer.py
```

## Docker Cleanup

To stop all containers and remove unused Docker resources:

```bash
./cleanup.sh
```

## Key Concepts

- **WindowManager** – Context manager that stores the original window, waits for and switches to a new window, and guarantees cleanup on exit.
- **Explicit waits** – Uses `WebDriverWait` instead of `time.sleep()` for reliability.
- **Set difference** – Identifies the new window by comparing current handles with the original, avoiding index assumptions.
- **Page Object Model** – `DemoPage` encapsulates page locators and actions used by tests.

## License

For educational use as part of the autotestman lesson series.
