"""
verify_result.py — post-run verification utility.

Run after: docker run --rm -v $(pwd)/reports:/app/reports uqap-tests:lesson76
Usage:     python3 utils/verify_result.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


REPORT_PATH = Path("reports/report.html")


def _first_count(html: str, patterns: tuple[str, ...]) -> int:
    """pytest-html v3 used '8 passed'; v4+ uses '<span class="passed">8 Passed,</span>'."""
    for pat in patterns:
        if (m := re.search(pat, html, flags=re.IGNORECASE)):
            return int(m.group(1))
    return 0


def _extract_summary(html: str) -> dict[str, int]:
    """Parse pytest-html report for pass/fail counts."""
    return {
        "passed": _first_count(
            html,
            (r'(\d+)\s+Passed', r'(\d+)\s+passed'),
        ),
        "failed": _first_count(
            html,
            (r'(\d+)\s+Failed', r'(\d+)\s+failed'),
        ),
        "errors": _first_count(
            html,
            (r'(\d+)\s+Errors', r'(\d+)\s+errors', r'(\d+)\s+error(?!s)'),
        ),
        "skipped": _first_count(
            html,
            (r'(\d+)\s+Skipped', r'(\d+)\s+skipped'),
        ),
    }


def verify_result() -> bool:
    """
    Return True if:
      - report.html exists
      - at least 1 test passed
      - 0 tests failed
    """
    if not REPORT_PATH.exists():
        print(f"\033[91m✖  Report not found: {REPORT_PATH}\033[0m")
        print("   Did you mount the volume? Try:")
        print("   docker run --rm -v $(pwd)/reports:/app/reports uqap-tests:lesson76")
        return False

    html = REPORT_PATH.read_text(encoding="utf-8")
    counts = _extract_summary(html)

    print("\n\033[1m── Test Result Verification ──────────────────────\033[0m")
    print(f"  \033[92m✔ Passed :\033[0m  {counts['passed']}")
    print(f"  \033[91m✖ Failed :\033[0m  {counts['failed']}")
    print(f"  \033[93m⚠ Errors :\033[0m  {counts['errors']}")
    print(f"  \033[2m  Skipped:\033[0m  {counts['skipped']}")
    print()

    if counts["failed"] > 0 or counts["errors"] > 0:
        print("\033[91m✖  VERIFICATION FAILED — tests failed inside Docker.\033[0m")
        return False

    if counts["passed"] == 0:
        print("\033[93m⚠  No tests ran. Check your pytest paths.\033[0m")
        return False

    print(f"\033[92m✔  VERIFIED — {counts['passed']} tests passed. Docker environment is healthy.\033[0m")
    return True


if __name__ == "__main__":
    success = verify_result()
    sys.exit(0 if success else 1)
