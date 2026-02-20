"""
TodoMVC Page Object - Refactored from Playwright Codegen
This demonstrates how to convert generated code into production-ready POM
"""
from playwright.async_api import Page, Locator, expect
from pages.base_page import BasePage
from typing import List


class TodoPage(BasePage):
    """Page Object for TodoMVC demo application"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        
        # Locators - defined once, reused everywhere
        self.new_todo_input: Locator = page.locator(".new-todo")
        self.todo_items: Locator = page.locator(".todo-list li")
        self.todo_count: Locator = page.locator(".todo-count")
        self.toggle_all: Locator = page.locator(".toggle-all")
        self.clear_completed: Locator = page.locator(".clear-completed")
        
        # Filter links
        self.filter_all: Locator = page.locator("a[href='#/']")
        self.filter_active: Locator = page.locator("a[href='#/active']")
        self.filter_completed: Locator = page.locator("a[href='#/completed']")
    
    async def add_todo(self, text: str):
        """Add a new todo item"""
        await self.new_todo_input.fill(text)
        await self.new_todo_input.press("Enter")
        # Wait for the item to appear in the list
        await self.page.wait_for_timeout(100)  # Small delay for animation
    
    async def add_multiple_todos(self, todos: List[str]):
        """Add multiple todo items"""
        for todo in todos:
            await self.add_todo(todo)
    
    async def get_todo_texts(self) -> List[str]:
        """Get all todo item texts"""
        return await self.todo_items.locator("label").all_text_contents()
    
    async def get_todo_count(self) -> int:
        """Get count of active todos"""
        count_text = await self.todo_count.text_content()
        # Extract number from "X items left" or "1 item left"
        return int(count_text.split()[0]) if count_text else 0

    async def get_visible_todo_count(self) -> int:
        """Count only visible todo items (filtered view may hide others in DOM)."""
        items = await self.todo_items.all()
        count = 0
        for item in items:
            if await item.is_visible():
                count += 1
        return count
    
    async def toggle_todo(self, index: int):
        """Toggle a todo's completed state by index (0-based)"""
        todo_item = self.todo_items.nth(index)
        await todo_item.locator(".toggle").click()
    
    async def toggle_all_todos(self):
        """Toggle all todos at once"""
        await self.toggle_all.click()
    
    async def delete_todo(self, index: int):
        """Delete a todo by index"""
        todo_item = self.todo_items.nth(index)
        # Hover to reveal delete button
        await todo_item.hover()
        await todo_item.locator(".destroy").click()
    
    async def clear_completed_todos(self):
        """Clear all completed todos"""
        await self.clear_completed.click()
    
    async def edit_todo(self, index: int, new_text: str):
        """Edit a todo item"""
        todo_item = self.todo_items.nth(index)
        await todo_item.dblclick()
        edit_input = todo_item.locator(".edit")
        await edit_input.fill(new_text)
        await edit_input.press("Enter")
    
    async def filter_by(self, filter_type: str):
        """Filter todos by: 'all', 'active', or 'completed'"""
        filters = {
            "all": self.filter_all,
            "active": self.filter_active,
            "completed": self.filter_completed
        }
        await filters[filter_type].click()
        await self.page.wait_for_timeout(150)  # Let filtered view update
    
    async def verify_todo_exists(self, text: str):
        """Verify a todo with given text exists"""
        todo = self.page.locator(f".todo-list li:has-text('{text}')")
        await expect(todo).to_be_visible()
    
    async def verify_todo_count(self, expected_count: int):
        """Verify the active todo count"""
        actual_count = await self.get_todo_count()
        assert actual_count == expected_count, f"Expected {expected_count} todos, got {actual_count}"
