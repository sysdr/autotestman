
"""
Verification script for Lesson 17 implementation
"""
import subprocess
import sys
from pathlib import Path


def run_tests():
    """Run pytest and return results"""
    result = subprocess.run(
        ["pytest", "tests/", "-v", "--tb=short"],
        capture_output=True,
        text=True
    )
    return result


def check_implementation():
    """Verify all required files exist"""
    required_files = [
        "utils/frame_handler.py",
        "pages/frame_test_page.py",
        "tests/conftest.py",
        "tests/test_frame_switching.py",
        "resources/test_frames.html"
    ]

    missing = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing.append(file_path)

    return missing


def main():
    print("=" * 60)
    print("LESSON 17: FRAME SWITCHING VERIFICATION")
    print("=" * 60)

    # Check file structure
    print("\n1. Checking file structure...")
    missing = check_implementation()
    if missing:
        print("❌ Missing files:")
        for f in missing:
            print(f"   - {f}")
        return False
    print("✓ All required files present")

    # Run tests
    print("\n2. Running test suite...")
    result = run_tests()

    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("✓ ALL VERIFICATIONS PASSED")
        print("=" * 60)
        print("\nKey Achievements:")
        print("  • Context managers ensure cleanup")
        print("  • Nested frames handled correctly")
        print("  • No context pollution between tests")
        print("  • Exception-safe frame switching")
        return True
    else:
        print("\n❌ Tests failed. Review output above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
