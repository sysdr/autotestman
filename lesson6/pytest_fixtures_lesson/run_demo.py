#!/usr/bin/env python3
"""Interactive demo showing fixture lifecycle."""
import subprocess
import sys
from pathlib import Path
from utils.file_helpers import count_temp_files, verify_cleanup


def print_section(title: str):
    """Print formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60)


def run_tests():
    """Run pytest and capture output."""
    print_section("Running PyTest Fixtures Demo")
    
    # Count temp files before tests
    before = count_temp_files()
    print(f"\n📊 Temp files before tests: {before}")
    
    # Run pytest with verbose output
    result = subprocess.run(
        ["pytest", "tests/", "-v", "-s"],
        capture_output=False
    )
    
    # Count temp files after tests
    after = count_temp_files()
    print(f"\n📊 Temp files after tests: {after}")
    
    # Verify cleanup
    print_section("Cleanup Verification")
    cleanup_success = verify_cleanup()
    
    # Summary
    print_section("Test Summary")
    if result.returncode == 0 and cleanup_success:
        print("✅ All tests passed")
        print("✅ All resources cleaned up")
        print("\n🎉 Fixture lifecycle working correctly!")
    else:
        print("❌ Some tests failed or cleanup incomplete")
        sys.exit(1)


if __name__ == "__main__":
    run_tests()
