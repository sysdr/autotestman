#!/usr/bin/env python3
"""
Side-by-Side Comparison: Print vs Logging
Run this to see the difference in output quality
"""

import sys
import subprocess
from pathlib import Path

def run_script(script_name: str) -> tuple[int, str]:
    """Execute a script and capture its return code"""
    print(f"\n{'='*70}")
    print(f"Running: {script_name}")
    print('='*70)
    
    result = subprocess.run(
        [sys.executable, script_name],
        capture_output=False,  # Let it print to console
        text=True
    )
    
    return result.returncode

def main():
    print("\n" + "="*70)
    print("LESSON 8: LOGGING FUNDAMENTALS - COMPARISON DEMO")
    print("="*70)
    
    # Run naive approach
    print("\n[1/2] NAIVE APPROACH (using print statements)")
    code1 = run_script("naive_print_approach.py")
    
    # Run proper approach
    print("\n[2/2] PROPER APPROACH (using logging module)")
    code2 = run_script("proper_logging_approach.py")
    
    # Summary
    print("\n" + "="*70)
    print("COMPARISON SUMMARY")
    print("="*70)
    print(f"Naive approach exit code: {code1}")
    print(f"Proper approach exit code: {code2}")
    print("\nKey Differences:")
    print("  1. Structured output with timestamps")
    print("  2. Severity levels (INFO, ERROR, WARNING)")
    print("  3. Automatic file logging (check logs/ directory)")
    print("  4. Module and function tracking")
    print("  5. Proper exception handling with tracebacks")
    print("="*70)
    
    print("\n✓ Check the logs/ directory for detailed execution logs")

if __name__ == "__main__":
    main()
