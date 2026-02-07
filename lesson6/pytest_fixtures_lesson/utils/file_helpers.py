"""Utility functions for file operations in tests."""
from pathlib import Path
from typing import List


def count_temp_files(directory: Path = Path("/tmp")) -> int:
    """
    Count remaining test files (useful for verifying cleanup).
    
    Args:
        directory: Directory to search for test files
        
    Returns:
        Number of test_*.txt files found
    """
    return len(list(directory.glob("test_*.txt")))


def verify_cleanup() -> bool:
    """
    Verify that all temp test files have been cleaned up.
    
    Returns:
        True if no test files remain, False otherwise
    """
    remaining = count_temp_files()
    if remaining > 0:
        print(f"⚠️  WARNING: {remaining} temp files not cleaned up!")
        return False
    
    print("✅ All temp files cleaned up successfully")
    return True


def list_temp_files(directory: Path = Path("/tmp")) -> List[Path]:
    """List all temporary test files."""
    return list(directory.glob("test_*.txt"))
