"""Test suite demonstrating pytest fixture patterns."""
import pytest
from pathlib import Path


def test_with_temp_file(temp_file: Path):
    """Test that uses the temp_file fixture."""
    assert temp_file.exists(), "Temp file should exist during test"
    
    # Write data to the file
    test_data = "Hello from automated test!"
    temp_file.write_text(test_data)
    
    # Verify data was written
    content = temp_file.read_text()
    assert content == test_data
    
    print(f"[TEST] Successfully wrote and read from {temp_file.name}")


def test_multiple_fixtures(temp_file: Path, test_data_dir: Path):
    """Test using multiple fixtures simultaneously."""
    assert temp_file.exists()
    assert test_data_dir.exists()
    assert test_data_dir.is_dir()
    
    # Move temp file into test directory
    new_location = test_data_dir / temp_file.name
    temp_file.rename(new_location)
    
    assert new_location.exists()
    assert not temp_file.exists()  # Original path should be gone
    
    print(f"[TEST] Moved file to {new_location}")


def test_file_with_content(temp_file_with_content: Path):
    """Test that the file comes pre-populated."""
    content = temp_file_with_content.read_text()
    lines = content.split("\n")
    
    assert len(lines) == 3, "Should have 3 lines"
    assert lines[0] == "Initial test data"
    
    # Append more data
    temp_file_with_content.write_text(content + "\nLine 4")
    
    updated = temp_file_with_content.read_text()
    assert "Line 4" in updated
    
    print(f"[TEST] Successfully modified pre-populated file")


def test_fixture_cleanup_on_failure(temp_file: Path):
    """
    Test that demonstrates cleanup happens even when test fails.
    
    Uncomment the assertion to see cleanup still occurs.
    """
    temp_file.write_text("Important data")
    print(f"[TEST] Wrote data to {temp_file}")
    
    # Uncomment to see cleanup happen despite failure:
    # assert False, "This test fails but cleanup still runs!"
    
    assert True  # Normal passing test


class TestFixtureScopes:
    """Grouped tests demonstrating fixture scoping."""
    
    def test_first(self, test_data_dir: Path):
        """First test in class."""
        marker_file = test_data_dir / "test1_marker.txt"
        marker_file.write_text("Test 1 was here")
        assert marker_file.exists()
        print(f"[TEST] Test 1 created marker in {test_data_dir}")
    
    def test_second(self, test_data_dir: Path):
        """Second test in class - shares the same test_data_dir."""
        # The marker from test_first should still exist
        marker_file = test_data_dir / "test1_marker.txt"
        
        # This demonstrates module scope - directory persists between tests
        assert marker_file.exists(), "Marker from previous test should exist"
        
        print(f"[TEST] Test 2 found test 1's marker (module scope working)")
