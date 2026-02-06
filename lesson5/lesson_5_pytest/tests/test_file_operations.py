"""
File Operations Tests
Demonstrates temp_workspace fixture for isolated file testing.
"""

import pytest
from pathlib import Path


def test_create_and_read_file(temp_workspace):
    """
    Tests basic file creation and reading.
    File exists only in this test's isolated workspace.
    """
    test_file = temp_workspace / "output.txt"
    test_content = "Hello, PyTest!"
    
    # Write file
    test_file.write_text(test_content)
    
    # Verify file exists
    assert test_file.exists(), f"File not created: {test_file}"
    
    # Verify content
    actual_content = test_file.read_text()
    assert actual_content == test_content, (
        f"Content mismatch. Expected: '{test_content}', Got: '{actual_content}'"
    )


def test_workspace_isolation(temp_workspace):
    """
    Verifies that each test gets a clean, isolated workspace.
    This test creates a file that won't interfere with other tests.
    """
    marker_file = temp_workspace / "isolation_test.txt"
    
    # This file should NOT exist (proves isolation from other tests)
    assert not marker_file.exists(), (
        "Workspace not isolated - file from previous test found"
    )
    
    # Create marker file
    marker_file.write_text("isolated")
    assert marker_file.exists()


def test_multiple_files_in_workspace(temp_workspace):
    """
    Tests creating multiple files in the same workspace.
    Demonstrates Path operations.
    """
    file_count = 5
    
    for i in range(file_count):
        file_path = temp_workspace / f"file_{i}.txt"
        file_path.write_text(f"Content {i}")
    
    # Verify all files created
    created_files = list(temp_workspace.glob("file_*.txt"))
    assert len(created_files) == file_count, (
        f"Expected {file_count} files, found {len(created_files)}"
    )
