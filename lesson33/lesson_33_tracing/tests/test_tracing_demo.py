"""
Example tests demonstrating Playwright tracing capabilities.
Run with: pytest tests/test_tracing_demo.py -v
"""

import pytest
from playwright.sync_api import Page, expect
from pathlib import Path


class TestTracingDemo:
    """Demonstrates tracing with both passing and failing tests"""
    
    def test_successful_navigation(self, traced_context, setup_trace_directory):
        """
        Test that PASSES - trace will be discarded.
        This demonstrates efficient trace management.
        """
        page = traced_context.new_page()
        
        # Navigate to a real website
        page.goto("https://playwright.dev")
        
        # Verify page loaded
        expect(page).to_have_title("Fast and reliable end-to-end testing for modern web apps | Playwright")
        
        # Click navigation link
        page.click("text=Get started")
        
        # Verify navigation
        expect(page).to_have_url("https://playwright.dev/docs/intro")
        
        page.close()
        # Trace automatically discarded since test passed
    
    def test_failing_element_search(self, traced_context, setup_trace_directory):
        """
        Test that FAILS intentionally - trace will be saved.
        This simulates a real CI failure scenario.
        """
        page = traced_context.new_page()
        
        page.goto("https://playwright.dev")
        
        # This selector doesn't exist - will fail and generate trace
        page.click("#this-element-does-not-exist", timeout=3000)
        
        page.close()
    
    def test_form_interaction_with_timing(self, traced_context, setup_trace_directory):
        """
        Test demonstrating form interaction - useful for debugging timing issues.
        This test PASSES but shows what gets captured in traces.
        """
        page = traced_context.new_page()
        
        # Use Playwright's own demo page
        page.goto("https://demo.playwright.dev/todomvc/")
        
        # Add todo item
        page.fill(".new-todo", "Write Playwright tests")
        page.press(".new-todo", "Enter")
        
        # Verify item added
        expect(page.locator(".todo-list li")).to_have_count(1)
        expect(page.locator(".todo-list li")).to_contain_text("Write Playwright tests")
        
        # Mark as complete
        page.click(".todo-list li .toggle")
        
        # Verify completion
        expect(page.locator(".todo-list li")).to_have_class("completed")
        
        page.close()
    
    @pytest.mark.parametrize("search_term", [
        "Python",
        "JavaScript", 
        "NonExistentLanguageThatWillFail"
    ])
    def test_search_functionality(self, traced_context, setup_trace_directory, search_term):
        """
        Parameterized test - each run gets its own trace.
        The third parameter will fail, demonstrating trace per test case.
        """
        page = traced_context.new_page()
        
        page.goto("https://playwright.dev")
        
        # Click search button
        page.click("button.DocSearch")
        
        # Type search term
        page.fill("input#docsearch-input", search_term)
        
        # Verify results appear (will fail for nonsense search term)
        expect(page.locator(".DocSearch-Hits")).to_be_visible(timeout=5000)
        
        page.close()


class TestAlwaysTraced:
    """Tests using always_traced_context fixture for detailed inspection"""
    
    def test_with_complete_trace(self, always_traced_context, setup_trace_directory):
        """
        This test saves trace even on success.
        Useful when you want to inspect passing tests.
        """
        page = always_traced_context.new_page()
        
        page.goto("https://playwright.dev/python")
        
        # Multiple actions to see in trace timeline
        page.click("text=Docs")
        page.click("text=API")
        page.click("text=Guides")
        
        page.close()
        # Trace saved regardless of pass/fail


if __name__ == "__main__":
    # Direct execution for quick testing
    pytest.main([__file__, "-v", "--tb=short"])
