#!/usr/bin/env python3
"""
NAIVE APPROACH: Using print() statements
This is how a junior developer typically writes automation code
"""

import json
from pathlib import Path
from datetime import datetime

def load_test_data(filepath: str) -> dict:
    """Load test configuration from JSON"""
    print(f"Loading test data from {filepath}")
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        print(f"Successfully loaded {len(data)} test cases")
        return data
    except FileNotFoundError:
        print(f"ERROR: File not found - {filepath}")
        return {}
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON - {e}")
        return {}

def validate_test_case(test_case: dict) -> bool:
    """Validate that a test case has required fields"""
    print(f"Validating test case: {test_case.get('name', 'Unknown')}")
    
    required_fields = ['name', 'url', 'expected_status']
    for field in required_fields:
        if field not in test_case:
            print(f"ERROR: Missing required field '{field}'")
            return False
        print(f"  Found field: {field}")
    
    print("Validation passed")
    return True

def execute_test_suite(data_file: str) -> None:
    """Execute a suite of tests"""
    print(f"\n{'='*50}")
    print(f"Starting test execution at {datetime.now()}")
    print(f"{'='*50}\n")
    
    test_data = load_test_data(data_file)
    
    if not test_data:
        print("ERROR: No test data loaded, aborting")
        return
    
    passed = 0
    failed = 0
    
    for test_case in test_data.get('tests', []):
        print(f"\nExecuting: {test_case['name']}")
        
        if validate_test_case(test_case):
            print(f"  Status: PASS")
            passed += 1
        else:
            print(f"  Status: FAIL")
            failed += 1
    
    print(f"\n{'='*50}")
    print(f"Test Summary:")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    print(f"  Total: {passed + failed}")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    execute_test_suite("data/test_config.json")
