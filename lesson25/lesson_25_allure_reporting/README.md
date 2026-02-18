# Lesson 25: Allure Reporting

## Overview
This workspace demonstrates production-grade test reporting using Allure Framework.

**To run after clone/pull:** install Chrome, ChromeDriver (in `drivers/chromedriver`), then `pip install -r requirements.txt`. See [Prerequisites](#prerequisites) and `requirements.txt` for details.

## Prerequisites

Install the following so the project runs after you clone/pull.

1. **Chrome browser (required for Selenium tests)**

**Linux / WSL (Ubuntu/Debian):**
```bash
# Option A: Google Chrome (recommended for /usr/bin/google-chrome)
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt-get update
sudo apt-get install -y google-chrome-stable

# Option B: Chromium (lighter; binary is usually /usr/bin/chromium or /usr/bin/chromium-browser)
sudo apt-get update
sudo apt-get install -y chromium-browser
```
If you use Chromium, set the binary path in `conftest.py` (see Troubleshooting).

**macOS:**
```bash
brew install --cask google-chrome
```

**Windows:**  
Install [Google Chrome](https://www.google.com/chrome/) and ensure it is on PATH.

2. **ChromeDriver (required for Selenium)**

Download [ChromeDriver 144 for linux64](https://chromedriver.chromium.org/downloads) (or the version matching your Chrome). Place the executable in the project:

```bash
mkdir -p drivers
# After downloading, move/copy the chromedriver binary to:
#   <project>/drivers/chromedriver
chmod +x drivers/chromedriver
```

3. **Python dependencies**

```bash
pip install -r requirements.txt
```

4. **Allure CLI (optional; only needed to generate/view HTML reports)**

**macOS:**
```bash
brew install allure
```

**Linux:**
```bash
# Download from https://github.com/allure-framework/allure2/releases
sudo tar -xzf allure-*.tgz -C /opt/
sudo ln -s /opt/allure-*/bin/allure /usr/bin/allure
```

**Windows:**
Download from [Allure releases](https://github.com/allure-framework/allure2/releases) and add to PATH.

## Quick Start – Steps to Perform

### Step 1: Go to the project directory
```bash
cd ~/git/autotestman/lesson25/lesson_25_allure_reporting
```

### Step 2: Activate virtual environment (if you use one)
```bash
source .venv/bin/activate
# or: source /home/systemdr03/automation-venv/bin/activate
```

### Step 3: Run tests and collect Allure results
```bash
pytest tests/ --alluredir=allure-results -v
```

### Step 4: Generate the HTML report
```bash
allure generate allure-results -o allure-report --clean
```

### Step 5: View the report

**Option A – WSL + browser on Windows (recommended)**  

1. From the **project root** (you must be in `lesson_25_allure_reporting`, not inside `allure-report`), start the server:
```bash
cd ~/git/autotestman/lesson25/lesson_25_allure_reporting
cd allure-report && python3 -m http.server 8765 --bind 0.0.0.0
```
2. Leave that terminal running. In another terminal, get your WSL IP:
```bash
hostname -I | awk '{print $1}'
```
3. In your **Windows** browser (Chrome, Edge, etc.), type in the address bar:
```text
http://<paste-the-IP-here>:8765
```
Example: if the command printed `172.17.32.19`, open `http://172.17.32.19:8765`.

**Option B – Allure built-in server (Linux-only or same machine)**  
```bash
allure serve allure-results -p 38063
```
Then open `http://127.0.0.1:38063` in a browser on the **same** machine (not from Windows if you're in WSL).

**Do not** open `allure-report/index.html` with `file://` – the report will stay on "Loading..." due to browser security.

## Project Structure
```
lesson_25_allure_reporting/
├── tests/
│   └── test_allure_demo.py      # Test suite with Allure annotations
├── pages/
│   ├── base_page.py             # Base page object
│   └── login_page.py            # Login page object
├── utils/
│   └── report_manager.py        # Report generation utilities
├── conftest.py                  # Pytest configuration + hooks
├── requirements.txt             # Python deps + setup notes (Chrome, ChromeDriver)
└── README.md
```
After running tests: `screenshots/`, `allure-results/`, and `allure-report/` are created (git-ignored).

## Allure Features Demonstrated

### 1. Test Organization
- `@allure.epic()` - High-level business objective
- `@allure.feature()` - Feature grouping
- `@allure.story()` - User story
- `@allure.severity()` - Priority level

### 2. Test Metadata
- `@allure.title()` - Human-readable test name
- `@allure.description()` - Detailed explanation
- `@allure.tag()` - Custom labels for filtering

### 3. Step Logging
```python
with allure.step("Step description"):
    # Test actions
```

### 4. Attachments
- Screenshots (auto-captured on failure)
- Page source HTML
- Browser logs
- Custom text/JSON data

### 5. Parametrized Tests
Allure automatically creates separate test cases for each parameter set.

## Report Sections

### Suites
Tests organized by file/class structure.

### Graphs
- **Status:** Pass/fail distribution
- **Severity:** Critical/blocker/normal/minor
- **Duration:** Execution time trends

### Timeline
Visual representation of parallel test execution.

### Behaviors
Tests grouped by Epic → Feature → Story hierarchy.

## CI/CD Integration

### GitHub Actions Example
```yaml
- name: Run tests
  run: pytest --alluredir=allure-results

- name: Generate report
  if: always()
  run: allure generate allure-results -o allure-report

- name: Upload report
  uses: actions/upload-artifact@v3
  with:
    name: allure-report
    path: allure-report/
```

### Jenkins Example
```groovy
stage('Test') {
    steps {
        sh 'pytest --alluredir=allure-results'
    }
}
stage('Report') {
    steps {
        allure includeProperties: false,
               jdk: '',
               results: [[path: 'allure-results']]
    }
}
```

## Advanced Usage

### Environment Info
Edit `allure-results/environment.properties` to add custom environment details.

### Historical Trends
Copy `allure-report/history` folder to `allure-results/history` before next run to preserve trends.

### Categories
Create `categories.json` in `allure-results/` to define custom failure categories:
```json
[
  {
    "name": "UI Failures",
    "matchedStatuses": ["failed"],
    "messageRegex": ".*ElementNotFound.*"
  }
]
```

## Troubleshooting

**No JSON files in allure-results/**
- Verify `allure-pytest` is installed
- Check pytest output for plugin errors

**Empty report**
- Ensure correct path: `allure generate allure-results` (not `allure-report`)

**Screenshots not appearing**
- Verify `conftest.py` fixture is running
- Check `screenshots/` folder for saved images

**"allure: command not found"**
- Install Allure CLI (see Prerequisites)
- Verify `allure --version` works

## Production Checklist
- [ ] Screenshots attached to all UI test failures
- [ ] Environment info populated
- [ ] Historical data preserved across runs
- [ ] Report hosted (S3/GCS) for stakeholder access
- [ ] Flaky tests identified via trend analysis
