#!/usr/bin/env python3
"""
Lesson 11: Browser Drivers & Navigation Setup Script
Generates a complete workspace for practicing browser automation.
"""

import os
from pathlib import Path
from typing import Dict

def create_directory_structure() -> Dict[str, Path]:
    """Create the lesson workspace structure."""
    base_dir = Path("lesson11_browser_drivers")
    
    directories = {
        "base": base_dir,
        "tests": base_dir / "tests",
        "pages": base_dir / "pages",
        "utils": base_dir / "utils",
    }
    
    for dir_path in directories.values():
        dir_path.mkdir(parents=True, exist_ok=True)
        
    return directories

def create_requirements_file(base_dir: Path) -> None:
    """Generate requirements.txt with pinned versions."""
    requirements = """selenium==4.16.0
webdriver-manager==4.0.1
pytest==7.4.3
"""
    (base_dir / "requirements.txt").write_text(requirements)

def create_page_object(pages_dir: Path) -> None:
    """Create the GoogleHomePage page object."""
    page_object_code = '''"""
Google Home Page Object
Encapsulates navigation and assertions for google.com
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GoogleHomePage:
    """Page Object for Google homepage."""
    
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.url = "https://www.google.com"
        self.timeout = 10
    
    def load(self) -> "GoogleHomePage":
        """
        Navigate to Google and wait for page to be ready.
        
        Returns:
            Self for method chaining
            
        Raises:
            TimeoutException: If page doesn't load within timeout
        """
        self.driver.get(self.url)
        
        # Explicit wait for page title to contain "Google"
        wait = WebDriverWait(self.driver, self.timeout)
        wait.until(EC.title_contains("Google"))
        
        return self
    
    def get_title(self) -> str:
        """
        Get the current page title.
        
        Returns:
            Page title as string
        """
        return self.driver.title
    
    def verify_loaded(self) -> bool:
        """
        Verify the page is properly loaded.
        
        Returns:
            True if title contains "Google"
        """
        return "Google" in self.driver.title
'''
    (pages_dir / "google_page.py").write_text(page_object_code)
    (pages_dir / "__init__.py").write_text("")

def create_driver_manager(utils_dir: Path) -> None:
    """Create a driver manager utility."""
    driver_manager_code = '''"""
WebDriver Manager Utility
Handles driver initialization and teardown with proper resource management.
"""

from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class DriverManager:
    """Manages WebDriver lifecycle."""
    
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.driver: Optional[webdriver.Chrome] = None
    
    def get_driver(self) -> webdriver.Chrome:
        """
        Initialize and return a Chrome WebDriver instance.
        
        Returns:
            Configured Chrome WebDriver
        """
        if self.driver:
            return self.driver
            
        options = Options()
        
        if self.headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
        
        # Production-ready options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.implicitly_wait(0)  # Force explicit waits only
        
        return self.driver
    
    def quit_driver(self) -> None:
        """Clean up driver resources."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                print(f"[WARNING] Error during driver cleanup: {e}")
            finally:
                self.driver = None
'''
    (utils_dir / "driver_manager.py").write_text(driver_manager_code)
    (utils_dir / "__init__.py").write_text("")

def create_test_file(tests_dir: Path) -> None:
    """Create the main test file."""
    test_code = '''"""
Test: Browser Navigation
Demonstrates proper browser automation with explicit waits.
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.driver_manager import DriverManager
from pages.google_page import GoogleHomePage


def run_test(headless: bool = False) -> bool:
    """
    Execute the navigation test.
    
    Args:
        headless: Run in headless mode (no visible browser)
        
    Returns:
        True if test passed
    """
    print("\\n" + "="*60)
    print("Lesson 11: Browser Drivers & Navigation Test")
    print("="*60 + "\\n")
    
    driver_manager = DriverManager(headless=headless)
    
    try:
        # Step 1: Initialize driver
        print("[SETUP] Initializing Chrome WebDriver...")
        driver = driver_manager.get_driver()
        print(f"[INFO] Driver initialized: {driver.capabilities['browserVersion']}")
        
        # Step 2: Navigate using Page Object
        print("[ACTION] Navigating to Google...")
        page = GoogleHomePage(driver)
        page.load()
        
        # Step 3: Get page title
        title = page.get_title()
        print(f"[RESULT] Page Title: '{title}'")
        
        # Step 4: Verify
        assert page.verify_loaded(), "Page verification failed"
        assert "Google" in title, f"Expected 'Google' in title, got '{title}'"
        
        print("[PASS] ✓ All assertions passed")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] ✗ Test failed: {e}")
        return False
        
    finally:
        # Step 5: Cleanup
        print("[CLEANUP] Closing browser...")
        driver_manager.quit_driver()
        print("="*60 + "\\n")


def verify_result() -> None:
    """
    Verification function to check test success.
    Demonstrates both headless and headed modes.
    """
    print("Running test in HEADED mode (you'll see the browser)...")
    result_headed = run_test(headless=False)
    
    print("\\n" + "-"*60 + "\\n")
    
    print("Running test in HEADLESS mode (no visible browser)...")
    result_headless = run_test(headless=True)
    
    print("\\n" + "="*60)
    print("VERIFICATION SUMMARY")
    print("="*60)
    print(f"Headed Mode:   {'PASS ✓' if result_headed else 'FAIL ✗'}")
    print(f"Headless Mode: {'PASS ✓' if result_headless else 'FAIL ✗'}")
    print("="*60 + "\\n")
    
    if result_headed and result_headless:
        print("🎉 All tests passed! Your browser automation is production-ready.")
    else:
        print("⚠️  Some tests failed. Review the logs above.")


if __name__ == "__main__":
    verify_result()
'''
    (tests_dir / "test_navigation.py").write_text(test_code)
    (tests_dir / "__init__.py").write_text("")

def create_readme(base_dir: Path) -> None:
    """Create README with instructions."""
    readme = """# Lesson 11: Browser Drivers & Navigation

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
"""
    (base_dir / "README.md").write_text(readme)

def generate_html_visualizer(base_dir: Path) -> None:
    """Create an HTML file to visualize the test flow."""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lesson 11: Browser Automation Flow</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            background: white;
            border-radius: 8px;
            padding: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #43b02a;
            padding-bottom: 10px;
        }
        .flow-step {
            display: flex;
            align-items: center;
            margin: 20px 0;
            padding: 15px;
            background: #f8f9fa;
            border-left: 4px solid #43b02a;
            border-radius: 4px;
        }
        .step-number {
            background: #43b02a;
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 15px;
        }
        .step-content {
            flex: 1;
        }
        .step-title {
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }
        .step-detail {
            color: #666;
            font-size: 14px;
        }
        .code {
            background: #2d2d2d;
            color: #f8f8f2;
            padding: 15px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
            overflow-x: auto;
            margin: 15px 0;
        }
        .highlight {
            color: #43b02a;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Lesson 11: Browser Automation Flow</h1>
        
        <div class="flow-step">
            <div class="step-number">1</div>
            <div class="step-content">
                <div class="step-title">Initialize WebDriver</div>
                <div class="step-detail">Auto-download ChromeDriver matching your Chrome version</div>
            </div>
        </div>
        
        <div class="flow-step">
            <div class="step-number">2</div>
            <div class="step-content">
                <div class="step-title">Navigate to URL</div>
                <div class="step-detail">driver.get() waits for document.readyState === 'complete'</div>
            </div>
        </div>
        
        <div class="flow-step">
            <div class="step-number">3</div>
            <div class="step-content">
                <div class="step-title">Explicit Wait</div>
                <div class="step-detail">Poll every 500ms until title contains "Google" (max 10s)</div>
            </div>
        </div>
        
        <div class="flow-step">
            <div class="step-number">4</div>
            <div class="step-content">
                <div class="step-title">Extract Data</div>
                <div class="step-detail">Get page title and verify expectations</div>
            </div>
        </div>
        
        <div class="flow-step">
            <div class="step-number">5</div>
            <div class="step-content">
                <div class="step-title">Clean Teardown</div>
                <div class="step-detail">driver.quit() closes browser and kills process</div>
            </div>
        </div>
        
        <h2>Key Concepts</h2>
        <div class="code">
<span class="highlight">NEVER DO THIS:</span>
driver.get("https://google.com")
time.sleep(5)  # ❌ Wastes time, causes flakiness

<span class="highlight">ALWAYS DO THIS:</span>
driver.get("https://google.com")
WebDriverWait(driver, 10).until(
    EC.title_contains("Google")
)  # ✓ Adaptive, fails fast, clear errors
        </div>
        
        <h2>Production Metrics</h2>
        <ul>
            <li><strong>Test Stability:</strong> &gt; 99% pass rate over 100 runs</li>
            <li><strong>Execution Time:</strong> &lt; 10 seconds for simple navigation</li>
            <li><strong>Resource Cleanup:</strong> Zero zombie processes after test</li>
        </ul>
    </div>
</body>
</html>
"""
    (base_dir / "flow_visualizer.html").write_text(html_content)

def main():
    """Main setup function."""
    print("\n" + "="*60)
    print("Setting up Lesson 11: Browser Drivers & Navigation")
    print("="*60 + "\n")
    
    # Create structure
    dirs = create_directory_structure()
    print(f"✓ Created directory: {dirs['base']}")
    
    # Generate files
    create_requirements_file(dirs['base'])
    print("✓ Generated requirements.txt")
    
    create_page_object(dirs['pages'])
    print("✓ Created Page Object: google_page.py")
    
    create_driver_manager(dirs['utils'])
    print("✓ Created Driver Manager utility")
    
    create_test_file(dirs['tests'])
    print("✓ Created test file: test_navigation.py")
    
    create_readme(dirs['base'])
    print("✓ Generated README.md")
    
    generate_html_visualizer(dirs['base'])
    print("✓ Created flow visualizer (HTML)")
    
    print("\n" + "="*60)
    print("Setup Complete!")
    print("="*60)
    print(f"\nNext steps:")
    print(f"  cd {dirs['base']}")
    print(f"  pip install -r requirements.txt")
    print(f"  python tests/test_navigation.py")
    print(f"\nView visualization: open flow_visualizer.html in browser")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()