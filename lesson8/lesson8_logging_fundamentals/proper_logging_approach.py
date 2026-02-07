#!/usr/bin/env python3
"""
PROPER APPROACH: Using Python's logging module
Production-ready implementation with structured logging
"""

import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

# Configure logging ONCE at module level
def setup_logging() -> logging.Logger:
    """
    Configure logging with both file and console handlers.
    This is the foundation of production observability.
    """
    # Create logs directory if it doesn't exist
    Path("logs").mkdir(exist_ok=True)
    
    # Create a logger instance
    logger = logging.getLogger("TestFramework")
    logger.setLevel(logging.DEBUG)  # Capture everything, filter at handler level
    
    # Prevent duplicate handlers if function is called multiple times
    if logger.handlers:
        return logger
    
    # Console Handler - Only INFO and above
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    
    # File Handler - Everything including DEBUG
    log_filename = f"logs/test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_format)
    
    # Attach handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

# Initialize logger at module level
logger = setup_logging()

def load_test_data(filepath: str) -> Optional[dict]:
    """Load test configuration from JSON with proper error logging"""
    logger.info(f"Loading test data from: {filepath}")
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        test_count = len(data.get('tests', []))
        logger.info(f"Successfully loaded {test_count} test cases")
        logger.debug(f"Raw data keys: {list(data.keys())}")
        
        return data
        
    except FileNotFoundError:
        logger.error(f"Test data file not found: {filepath}")
        logger.debug(f"Current working directory: {Path.cwd()}")
        return None
        
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON format in {filepath}")
        logger.exception("JSON decode error details:")  # Includes full traceback
        return None
        
    except Exception as e:
        logger.critical(f"Unexpected error loading test data: {type(e).__name__}")
        logger.exception("Full traceback:")
        return None

def validate_test_case(test_case: dict) -> bool:
    """Validate that a test case has required fields"""
    test_name = test_case.get('name', 'UNNAMED_TEST')
    logger.debug(f"Validating test case: {test_name}")
    
    required_fields = ['name', 'url', 'expected_status']
    missing_fields = [field for field in required_fields if field not in test_case]
    
    if missing_fields:
        logger.error(f"Test '{test_name}' missing required fields: {missing_fields}")
        logger.debug(f"Available fields: {list(test_case.keys())}")
        return False
    
    logger.debug(f"Test '{test_name}' validation passed")
    return True

def execute_test_suite(data_file: str) -> dict:
    """
    Execute a suite of tests with comprehensive logging.
    Returns a results dictionary for programmatic verification.
    """
    logger.info("="*60)
    logger.info(f"TEST SUITE EXECUTION STARTED")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info("="*60)
    
    test_data = load_test_data(data_file)
    
    if test_data is None:
        logger.critical("Cannot proceed without test data - aborting suite")
        return {"passed": 0, "failed": 0, "total": 0, "status": "ABORTED"}
    
    results = {"passed": 0, "failed": 0, "skipped": 0}
    
    tests = test_data.get('tests', [])
    logger.info(f"Found {len(tests)} tests to execute")
    
    for idx, test_case in enumerate(tests, 1):
        test_name = test_case.get('name', f'Test_{idx}')
        logger.info(f"[{idx}/{len(tests)}] Executing: {test_name}")
        
        if validate_test_case(test_case):
            logger.info(f"✓ {test_name} - PASSED")
            results["passed"] += 1
        else:
            logger.warning(f"✗ {test_name} - FAILED")
            results["failed"] += 1
    
    results["total"] = results["passed"] + results["failed"] + results["skipped"]
    
    logger.info("="*60)
    logger.info("TEST SUITE EXECUTION COMPLETED")
    logger.info(f"Results: {results['passed']} passed, {results['failed']} failed, {results['total']} total")
    
    pass_rate = (results['passed'] / results['total'] * 100) if results['total'] > 0 else 0
    logger.info(f"Pass Rate: {pass_rate:.1f}%")
    
    if results['failed'] > 0:
        logger.warning(f"Suite completed with failures")
    else:
        logger.info("All tests passed successfully")
    
    logger.info("="*60)
    
    return results

if __name__ == "__main__":
    results = execute_test_suite("data/test_config.json")
    
    # Exit with appropriate code for CI/CD integration
    exit_code = 0 if results["failed"] == 0 else 1
    logger.info(f"Exiting with code: {exit_code}")
    exit(exit_code)
