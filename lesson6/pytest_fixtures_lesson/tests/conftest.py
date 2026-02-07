"""Shared pytest fixtures for file manipulation tests."""
import pytest
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Generator
import uuid


@pytest.fixture
def temp_file() -> Generator[Path, None, None]:
    """
    Creates a temporary file before test, deletes after.
    
    Yields:
        Path: Path object pointing to the temporary file
        
    Example:
        def test_something(temp_file):
            temp_file.write_text("data")
            assert temp_file.exists()
    """
    # Setup phase: Create unique temporary file
    temp_path = Path(f"/tmp/test_{uuid.uuid4().hex[:8]}.txt")
    temp_path.touch()
    
    print(f"\n[SETUP] Created temp file: {temp_path}")
    
    # Yield control to the test
    yield temp_path
    
    # Teardown phase: Always cleanup (even if test fails)
    if temp_path.exists():
        temp_path.unlink()
        print(f"[TEARDOWN] Deleted temp file: {temp_path}")
    else:
        print(f"[TEARDOWN] File already deleted: {temp_path}")


@pytest.fixture(scope="module")
def test_data_dir() -> Generator[Path, None, None]:
    """
    Module-scoped fixture: Creates directory once for all tests in module.
    
    Demonstrates fixture scoping for expensive setup operations.
    """
    data_dir = Path(f"/tmp/test_data_{uuid.uuid4().hex[:8]}")
    data_dir.mkdir(exist_ok=True)
    
    print(f"\n[MODULE SETUP] Created test directory: {data_dir}")
    
    yield data_dir
    
    # Cleanup entire directory tree
    import shutil
    if data_dir.exists():
        shutil.rmtree(data_dir)
        print(f"[MODULE TEARDOWN] Deleted directory: {data_dir}")


@pytest.fixture
def temp_file_with_content() -> Generator[Path, None, None]:
    """
    Fixture that provides a file with pre-populated content.
    
    Demonstrates setup logic before yield.
    """
    temp_path = Path(f"/tmp/test_{uuid.uuid4().hex[:8]}.txt")
    
    # Write initial content during setup
    temp_path.write_text("Initial test data\nLine 2\nLine 3")
    
    print(f"\n[SETUP] Created file with content: {temp_path}")
    
    yield temp_path
    
    # Cleanup
    if temp_path.exists():
        temp_path.unlink()
        print(f"[TEARDOWN] Cleaned up: {temp_path}")
