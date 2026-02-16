"""
tests/test_kanban_drag.py
Test suite for drag-and-drop functionality.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.kanban_page import KanbanPage
import sys
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def driver(request):
    """Create WebDriver instance with cleanup."""
    print("\n🔧 SETUP: Initializing browser...")
    print("   → Setting up Chrome options...")
    options = Options()

    # Check for headless mode
    if request.config.getoption("--headless", default=False):
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        print("   → Running in headless mode")
    else:
        print("   → Running in visible mode (you can see the browser)")

    # Required for CI/CD environments
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    # Use webdriver-manager to automatically handle ChromeDriver
    print("   → Downloading/checking ChromeDriver...")
    service = Service(ChromeDriverManager().install())
    print("   → Starting Chrome browser...")
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(1)
    print("   ✅ Browser ready!\n")
    time.sleep(0.3)  # Brief pause

    yield driver

    print("\n🧹 CLEANUP: Closing browser...")
    driver.quit()
    print("   ✅ Browser closed successfully")


@pytest.mark.timeout(60)
def test_drag_photo_to_trash(driver):
    """
    Test: Drag 2 photos from gallery to trash.

    Success Criteria:
    1. First photo successfully moves to trash
    2. Second photo successfully moves to trash
    3. Trash count increases by 2
    4. Photos are verified in trash container
    """
    print("\n" + "="*70)
    print("🧪 TEST STARTING: Drag 2 Photos to Trash")
    print("="*70 + "\n")
    
    # Arrange
    print("📋 STEP 1: Setting up test environment...")
    print("   → Creating page object...")
    page = KanbanPage(driver)
    time.sleep(0)  # Wait to see the step
    
    print("   → Opening demo website...")
    page.open()
    print("   ✅ Page loaded successfully!\n")
    time.sleep(0.5)  # Brief pause
    
    print("📋 STEP 2: Capturing initial state...")
    initial_trash_count = page.get_trash_item_count()
    print(f"   📸 Initial trash count: {initial_trash_count}\n")
    time.sleep(0.5)  # Brief pause
    
    # Act - Drag first photo
    print("📋 STEP 3: Performing first drag-and-drop operation...")
    print("   🖱️  Dragging photo #1 from gallery to trash...")
    drag_success_1 = page.drag_photo_to_trash()
    print("   ✅ First drag operation completed!\n")
    time.sleep(0.5)  # Brief pause
    
    # Verify first drag
    print("📋 STEP 4: Verifying first drag operation...")
    assert drag_success_1, "First drag operation failed"
    print("   ✅ First drag operation was successful")
    
    count_after_first = page.get_trash_item_count()
    print(f"   📊 Trash count after first drag: {count_after_first}")
    assert count_after_first == initial_trash_count + 1, \
        f"Expected {initial_trash_count + 1} items after first drag, got {count_after_first}"
    print("   ✅ First drag verification passed!\n")
    time.sleep(1)  # Wait before second drag
    
    # Act - Drag second photo
    print("📋 STEP 5: Performing second drag-and-drop operation...")
    print("   🖱️  Dragging photo #2 from gallery to trash...")
    drag_success_2 = page.drag_photo_to_trash()  # Second photo is now first in gallery
    print("   ✅ Second drag operation completed!\n")
    time.sleep(0.5)  # Brief pause
    
    # Assert - Verify second drag
    print("📋 STEP 6: Verifying second drag operation...")
    assert drag_success_2, "Second drag operation failed"
    print("   ✅ Second drag operation was successful\n")
    time.sleep(0.3)  # Brief pause
    
    print("📋 STEP 7: Verifying final trash count...")
    final_trash_count = page.get_trash_item_count()
    print(f"   📊 Final trash count: {final_trash_count}")
    print(f"   📊 Expected count: {initial_trash_count + 2}")
    assert final_trash_count == initial_trash_count + 2, \
        f"Expected {initial_trash_count + 2} items, got {final_trash_count}"
    print("   ✅ Trash count verification passed!\n")
    time.sleep(0.5)  # Brief pause
    
    print("📋 STEP 8: Verifying photos are in trash container...")
    verification_result = page.verify_photo_in_trash()
    assert verification_result, "Photos not found in trash container"
    print("   ✅ Photo verification passed!\n")
    time.sleep(0.5)  # Brief pause
    
    print("="*70)
    print("✅ TEST PASSED: 2 Photos successfully dragged to trash")
    print("="*70 + "\n")


def pytest_addoption(parser):
    """Add custom command line options."""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )