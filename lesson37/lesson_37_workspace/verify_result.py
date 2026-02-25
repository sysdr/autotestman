"""
verify_result.py — Post-test verification for Lesson 37.
Run after pytest to confirm the lesson was implemented correctly.
"""
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent

CHECKS: list[tuple[str, bool, str]] = []


def check(label: str, passed: bool, detail: str = "") -> None:
    CHECKS.append((label, passed, detail))
    icon  = "✅" if passed else "❌"
    extra = f" — {detail}" if detail else ""
    print(f"  {icon}  {label}{extra}")


def run_verification() -> None:
    print("\n══ LESSON 37 VERIFICATION ════════════════════════════════")

    # 1. No time.sleep() usage in test file (docstrings saying "NEVER time.sleep()" are OK)
    test_file = ROOT / "tests" / "test_chat_multicontext.py"
    source = test_file.read_text()
    no_sleep = True
    for line in source.splitlines():
        if "time.sleep" not in line:
            continue
        if line.strip().startswith("#"):
            continue
        if "NEVER" in line or "don't" in line or "do not" in line:
            continue
        no_sleep = False
        break
    check("No time.sleep() in test file", no_sleep,
          "Found time.sleep() usage — remove it" if not no_sleep else "clean")

    # 2. Test file uses expect() assertions
    uses_expect = "expect(" in source
    check("Uses expect() for assertions", uses_expect,
          "Playwright auto-waiting not detected")

    # 3. Run pytest and measure wall-clock time
    start = time.perf_counter()
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short", "-q"],
        capture_output=True, text=True, cwd=str(ROOT)
    )
    elapsed = time.perf_counter() - start
    tests_passed = result.returncode == 0
    check("All pytest tests pass", tests_passed,
          result.stdout.split("\n")[-3] if not tests_passed else "✓")
    check(f"Total runtime < 30s (actual: {elapsed:.1f}s)", elapsed < 30,
          "Optimise fixture scope if slow")

    # ── Summary ────────────────────────────────────────────────────────
    passed = sum(1 for _, p, _ in CHECKS if p)
    total  = len(CHECKS)
    print(f"\n  {'✅ VERIFICATION PASSED' if passed == total else '❌ VERIFICATION FAILED'}: "
          f"{passed}/{total} checks passed. Lesson 37 {'complete' if passed == total else 'needs work'}.")
    print("══════════════════════════════════════════════════════════\n")
    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    run_verification()
