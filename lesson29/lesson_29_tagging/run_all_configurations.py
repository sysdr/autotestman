#!/usr/bin/env python3
"""
Utility script to run tests with different marker configurations
"""
import subprocess
import sys
from pathlib import Path


def run_command(cmd: list, description: str) -> int:
    """Run a shell command and return exit code"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    print(f"Command: {' '.join(cmd)}\n")

    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    return result.returncode


def main():
    """Run different test configurations"""

    configs = [
        (["pytest", "-m", "smoke", "-v"], 
         "Running SMOKE tests (fast feedback)"),

        (["pytest", "-m", "regression", "-v"], 
         "Running REGRESSION tests (comprehensive)"),

        (["pytest", "-m", "api", "-v"], 
         "Running API tests only"),

        (["pytest", "-m", "smoke and api", "-v"], 
         "Running SMOKE + API intersection"),

        (["pytest", "-m", "not slow", "-v"], 
         "Running all tests EXCEPT slow ones"),
    ]

    results = {}

    for cmd, desc in configs:
        exit_code = run_command(cmd, desc)
        results[desc] = exit_code

    # Summary
    print(f"\n{'='*60}")
    print("📊 EXECUTION SUMMARY")
    print(f"{'='*60}")

    for desc, code in results.items():
        status = "✓ PASSED" if code == 0 else "✗ FAILED"
        print(f"{status} - {desc}")

    return 0 if all(code == 0 for code in results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())