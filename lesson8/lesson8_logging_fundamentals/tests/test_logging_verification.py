#!/usr/bin/env python3
"""
Verification Test: Ensures logging configuration works correctly
"""

import logging
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.logging_config import get_logger

def test_logger_creation():
    """Test that logger can be created"""
    logger = get_logger("test_module")
    assert logger is not None, "Logger should not be None"
    assert logger.name == "test_module", f"Expected 'test_module', got '{logger.name}'"
    print("✓ Logger creation test passed")

def test_log_levels():
    """Test that different log levels work"""
    logger = get_logger("test_levels", level=logging.DEBUG)
    
    logger.debug("This is a DEBUG message")
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    
    print("✓ Log levels test passed")

def test_file_logging():
    """Test that logs are written to file"""
    logger = get_logger("test_file")
    logger.info("Testing file logging")
    
    log_dir = Path("logs")
    assert log_dir.exists(), "Logs directory should exist"
    
    log_files = list(log_dir.glob("session_*.log"))
    assert len(log_files) > 0, "Should have at least one log file"
    
    print(f"✓ File logging test passed - Found {len(log_files)} log file(s)")

def run_all_tests():
    """Run all verification tests"""
    print("="*60)
    print("Running Logging Verification Tests")
    print("="*60 + "\n")
    
    tests = [
        test_logger_creation,
        test_log_levels,
        test_file_logging
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test_func.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__} crashed: {e}")
            failed += 1
    
    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed")
    print("="*60)
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
