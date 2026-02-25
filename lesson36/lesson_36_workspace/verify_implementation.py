#!/usr/bin/env python3
"""
Verification script for Lesson 36.
Runs the test suite and validates the storage state pattern.
"""

import subprocess
import sys
from pathlib import Path
import json


def verify_auth_state_file() -> bool:
    """Check if auth_state.json was created"""
    auth_file = Path("auth_state.json")
    if not auth_file.exists():
        print("❌ auth_state.json not found")
        return False

    # Validate JSON structure
    with open(auth_file) as f:
        state = json.load(f)

    if "cookies" not in state:
        print("❌ auth_state.json missing 'cookies' field")
        return False

    if "origins" not in state:
        print("❌ auth_state.json missing 'origins' field")
        return False

    print(f"✅ auth_state.json valid ({len(state['cookies'])} cookies)")
    return True


def run_tests() -> bool:
    """Execute the test suite"""
    print("\n🧪 Running test suite...\n")
    result = subprocess.run(
        ["pytest", "tests/", "-v", "--tb=short"],
        capture_output=False
    )
    return result.returncode == 0


def main() -> int:
    """Run verification checks"""
    print("=" * 60)
    print("Lesson 36: Authenticated State Storage - Verification")
    print("=" * 60)

    # Run tests (this will generate auth_state.json on first run)
    tests_passed = run_tests()

    if not tests_passed:
        print("\n❌ Tests failed")
        return 1

    # Verify state file was created
    print("\n📋 Verifying storage state file...")
    state_valid = verify_auth_state_file()

    if not state_valid:
        return 1

    print("\n" + "=" * 60)
    print("✅ All verifications passed!")
    print("=" * 60)
    print("\nKey Takeaways:")
    print("  • Authentication executed ONCE (session-scoped fixture)")
    print("  • State saved to auth_state.json")
    print("  • All tests reused cached state (0 login overhead)")
    print("  • Pattern scales to 1000+ tests efficiently")

    return 0


if __name__ == "__main__":
    sys.exit(main())