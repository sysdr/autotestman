"""
Test Suite for TodoMVC - Refactored from Codegen Output
This demonstrates production-ready tests vs raw codegen
"""
import pytest
from playwright.async_api import Page, expect
from pages.todo_page import TodoPage


@pytest.mark.asyncio
class TestTodoBasicOperations:
    """Basic CRUD operations on todos"""
    
    async def test_add_single_todo(self, todo_page: TodoPage):
        """Test adding a single todo item"""
        # Arrange
        todo_text = "Buy groceries"
        
        # Act
        await todo_page.add_todo(todo_text)
        
        # Assert
        await todo_page.verify_todo_exists(todo_text)
        await todo_page.verify_todo_count(1)
    
    async def test_add_multiple_todos(self, todo_page: TodoPage):
        """Test adding multiple todo items"""
        # Arrange
        todos = ["Task 1", "Task 2", "Task 3"]
        
        # Act
        await todo_page.add_multiple_todos(todos)
        
        # Assert
        todo_texts = await todo_page.get_todo_texts()
        assert todo_texts == todos
        await todo_page.verify_todo_count(3)
    
    async def test_toggle_todo_completion(self, todo_page: TodoPage):
        """Test marking a todo as complete"""
        # Arrange
        await todo_page.add_todo("Complete this task")
        
        # Act
        await todo_page.toggle_todo(0)
        
        # Assert
        await todo_page.verify_todo_count(0)  # Should be 0 active items
    
    async def test_delete_todo(self, todo_page: TodoPage):
        """Test deleting a todo item"""
        # Arrange
        await todo_page.add_multiple_todos(["Keep this", "Delete this"])
        
        # Act
        await todo_page.delete_todo(1)
        
        # Assert
        todo_texts = await todo_page.get_todo_texts()
        assert len(todo_texts) == 1
        assert "Keep this" in todo_texts
        assert "Delete this" not in todo_texts
    
    async def test_edit_todo(self, todo_page: TodoPage):
        """Test editing a todo item"""
        # Arrange
        original_text = "Original task"
        new_text = "Updated task"
        await todo_page.add_todo(original_text)
        
        # Act
        await todo_page.edit_todo(0, new_text)
        
        # Assert
        await todo_page.verify_todo_exists(new_text)
        todo_texts = await todo_page.get_todo_texts()
        assert new_text in todo_texts
        assert original_text not in todo_texts


@pytest.mark.asyncio
class TestTodoFiltering:
    """Test filtering functionality"""
    
    async def test_filter_active_todos(self, todo_page: TodoPage):
        """Test filtering to show only active todos"""
        # Arrange
        await todo_page.add_multiple_todos(["Active task", "Will complete"])
        await todo_page.toggle_todo(1)  # Complete second task
        
        # Act
        await todo_page.filter_by("active")
        
        # Assert (count only visible items; filtered-out are hidden in DOM)
        visible_count = await todo_page.get_visible_todo_count()
        assert visible_count == 1
    
    async def test_filter_completed_todos(self, todo_page: TodoPage):
        """Test filtering to show only completed todos"""
        # Arrange
        await todo_page.add_multiple_todos(["Task 1", "Task 2"])
        await todo_page.toggle_todo(0)  # Complete first task
        
        # Act
        await todo_page.filter_by("completed")
        
        # Assert (count only visible items; filtered-out are hidden in DOM)
        visible_count = await todo_page.get_visible_todo_count()
        assert visible_count == 1
    
    async def test_clear_completed(self, todo_page: TodoPage):
        """Test clearing all completed todos"""
        # Arrange
        await todo_page.add_multiple_todos(["Task 1", "Task 2", "Task 3"])
        await todo_page.toggle_todo(0)
        await todo_page.toggle_todo(1)
        
        # Act
        await todo_page.clear_completed_todos()
        
        # Assert
        todo_texts = await todo_page.get_todo_texts()
        assert len(todo_texts) == 1
        await todo_page.verify_todo_count(1)


@pytest.mark.asyncio
class TestTodoBulkOperations:
    """Test bulk operations"""
    
    async def test_toggle_all_on(self, todo_page: TodoPage):
        """Test completing all todos at once"""
        # Arrange
        await todo_page.add_multiple_todos(["Task 1", "Task 2", "Task 3"])
        
        # Act
        await todo_page.toggle_all_todos()
        
        # Assert
        await todo_page.verify_todo_count(0)  # All completed
    
    async def test_toggle_all_off(self, todo_page: TodoPage):
        """Test uncompleting all todos"""
        # Arrange
        await todo_page.add_multiple_todos(["Task 1", "Task 2"])
        await todo_page.toggle_all_todos()  # Complete all
        
        # Act
        await todo_page.toggle_all_todos()  # Uncomplete all
        
        # Assert
        await todo_page.verify_todo_count(2)  # All active again
