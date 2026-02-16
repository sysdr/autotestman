"""
pages/kanban_page.py
Page Object Model for Kanban board demo.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.drag_drop_helper import DragDropHelper
import time


class KanbanPage:
    """Page Object for Kanban board interactions."""

    # Demo site URL (public Kanban board example)
    URL = "https://www.globalsqa.com/demo-site/draganddrop/"

    # Locators
    IFRAME = (By.CSS_SELECTOR, "iframe.demo-frame")
    PHOTO_1 = (By.CSS_SELECTOR, "#gallery li.ui-draggable:first-child")
    PHOTO_2 = (By.XPATH, "//img[@alt='The chalet at the Green mountain lake']")
    TRASH = (By.ID, "trash")
    GALLERY = (By.ID, "gallery")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.drag_helper = DragDropHelper(driver)

    def open(self) -> "KanbanPage":
        """Navigate to the Kanban demo page."""
        print("      → Navigating to: " + self.URL)
        self.driver.get(self.URL)
        time.sleep(0.3)  # Brief pause
        
        print("      → Looking for iframe...")
        iframe = self.wait.until(EC.presence_of_element_located(self.IFRAME))
        print("      → Switching to iframe context...")
        self.driver.switch_to.frame(iframe)
        print("      ✅ Switched to demo iframe")
        time.sleep(0.3)  # Brief pause
        
        print("      → Waiting for gallery to load...")
        self.wait.until(EC.presence_of_element_located(self.GALLERY))
        print("      → Waiting for draggable elements...")
        self.wait.until(EC.presence_of_element_located(self.PHOTO_1))
        print("      ✅ Draggable element found")
        return self

    def drag_photo_to_trash(self) -> bool:
        """
        Drag first photo to trash.

        Returns:
            True if drag was successful
        """
        print("      → Locating source element (photo in gallery)...")
        print("      → Locating target element (trash container)...")
        print("      → Executing drag-and-drop action...")
        result = self.drag_helper.drag_and_drop_with_retry(
            self.PHOTO_1,
            self.TRASH
        )
        return result
    
    def drag_photo_by_index_to_trash(self, index: int = 1) -> bool:
        """
        Drag a photo by its index position to trash.
        
        Args:
            index: 1-based index of the photo (1 = first photo, 5 = second photo, etc.)
            
        Returns:
            True if drag was successful
        """
        photo_locator = (By.CSS_SELECTOR, f"#gallery li.ui-draggable:nth-child({index})")
        return self.drag_helper.drag_and_drop_with_retry(
            photo_locator,
            self.TRASH
        )

    def verify_photo_in_trash(self) -> bool:
        """
        Verify photo is in trash container.

        Returns:
            True if photo is in trash
        """
        trash = self.driver.find_element(*self.TRASH)
        # Check if trash contains any li elements (photos)
        items = trash.find_elements(By.TAG_NAME, "li")
        # Also check if there are any images in the trash
        images = trash.find_elements(By.TAG_NAME, "img")
        result = len(items) > 0 or len(images) > 0
        print(f"VERIFY: Photo is in trash: {result} (found {len(items)} li items, {len(images)} images)")
        return result

    def get_trash_item_count(self) -> int:
        """Get number of items in trash."""
        trash = self.driver.find_element(*self.TRASH)
        items = trash.find_elements(By.TAG_NAME, "li")
        count = len(items)
        print(f"📊 Trash contains {count} items")
        return count