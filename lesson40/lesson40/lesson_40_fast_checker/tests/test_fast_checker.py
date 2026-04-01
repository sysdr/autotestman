# tests/test_fast_checker.py
"""
Lesson 40: The Fast Checker — Main Test Suite

Demonstrates:
- async pytest fixtures (pytest-asyncio in auto mode)
- Fan-Out / Fan-In link checking via APIRequestContext
- Structured reporting with pass/fail assertions
"""

import pytest
import time
from pathlib import Path
from playwright.async_api import APIRequestContext

from utils.link_checker import run_fast_check, generate_html_report, CheckReport

# ── Configuration ────────────────────────────────────────────────────────────
TARGET_URL = "https://example.com"       # Safe, public, always-up test target
REPORTS_DIR = Path(__file__).parent.parent / "reports"

# Production thresholds
MAX_EXECUTION_SECONDS = 30.0             # Generous for CI network variability
MIN_SUCCESS_RATE = 95.0                  # 95%+ links must be 200 OK
MIN_LINK_COUNT = 1                       # At least 1 link must be found


# ── Tests ─────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_all_links_are_200(api_context: APIRequestContext) -> None:
    """
    PRIMARY TEST: Validate all homepage links return HTTP 200 in parallel.

    This test WILL FAIL if:
    - Success rate drops below MIN_SUCCESS_RATE
    - Execution takes longer than MAX_EXECUTION_SECONDS
    - Zero links are found (selector/network problem)
    """
    REPORTS_DIR.mkdir(exist_ok=True)

    # Execute the fast check
    report: CheckReport = await run_fast_check(api_context, TARGET_URL)

    # ── Visualize in CLI ───────────────────────────────────────────────────
    print(f"\n{'─'*60}")
    print(f"  🔗 Fast Checker Report")
    print(f"{'─'*60}")
    print(f"  Target          : {report.target_url}")
    print(f"  Links found     : {report.total}")
    print(f"  ✅ Passed       : {report.passed}")
    print(f"  ❌ Failed       : {report.failed}")
    print(f"  Success rate    : {report.success_rate:.1f}%")
    print(f"  Execution time  : {report.execution_time_s}s")
    print(f"{'─'*60}")

    if report.failed > 0:
        print("  FAILED LINKS:")
        for r in report.results:
            if not r.ok:
                print(f"    [{r.status or 'ERR'}] {r.url[:70]}")
                if r.error:
                    print(f"          error: {r.error[:80]}")
    print()

    # ── Generate HTML report ───────────────────────────────────────────────
    report_path = REPORTS_DIR / "link_check_report.html"
    generate_html_report(report, report_path)
    print(f"  📄 HTML report  : {report_path}")

    # ── Assertions (production thresholds) ────────────────────────────────
    assert report.total >= MIN_LINK_COUNT, (
        f"Expected at least {MIN_LINK_COUNT} links, found {report.total}. "
        "Homepage scraping may have failed."
    )
    assert report.execution_time_s <= MAX_EXECUTION_SECONDS, (
        f"Execution took {report.execution_time_s}s — exceeded {MAX_EXECUTION_SECONDS}s limit. "
        "Check for sequential execution or network bottleneck."
    )
    assert report.success_rate >= MIN_SUCCESS_RATE, (
        f"Success rate {report.success_rate:.1f}% below threshold {MIN_SUCCESS_RATE}%. "
        f"Failed links:\n" +
        "\n".join(f"  [{r.status}] {r.url}" for r in report.results if not r.ok)
    )


@pytest.mark.asyncio
async def test_parallelism_is_faster_than_sequential(api_context: APIRequestContext) -> None:
    """
    PROOF TEST: Verify that parallel execution is measurably faster than sequential.

    This test checks 5 known URLs sequentially vs. in parallel and asserts
    that parallel is at least 1.1x faster (tolerant of network variance).
    """
    from utils.link_checker import _check_single_link
    import asyncio

    # Use well-known, reliable URLs
    test_urls = [
        "https://example.com",
        "https://www.iana.org/domains/reserved",
        "https://httpbin.org/status/200",
        "https://httpbin.org/delay/0",
        "https://httpbin.org/get",
    ]

    semaphore = asyncio.Semaphore(10)

    # ── Sequential timing ─────────────────────────────────────────────────
    seq_start = time.perf_counter()
    for url in test_urls:
        await _check_single_link(api_context, url, semaphore)
    seq_time = time.perf_counter() - seq_start

    # ── Parallel timing ───────────────────────────────────────────────────
    par_start = time.perf_counter()
    tasks = [_check_single_link(api_context, url, semaphore) for url in test_urls]
    await asyncio.gather(*tasks)
    par_time = time.perf_counter() - par_start

    speedup = seq_time / par_time if par_time > 0 else 1.0

    print(f"\n  Sequential: {seq_time:.2f}s")
    print(f"  Parallel  : {par_time:.2f}s")
    print(f"  Speedup   : {speedup:.1f}x")

    # Parallel should be meaningfully faster; use 1.1x to tolerate network variance
    assert speedup >= 1.1, (
        f"Expected parallel to be at least 1.1x faster than sequential. "
        f"Got {speedup:.2f}x. This suggests the async concurrency is not working."
    )


def verify_result(report_path: Path | None = None) -> bool:
    """
    Standalone verification function — can be called outside pytest.
    Returns True if the last generated report shows >= 95% success rate.
    """
    if report_path is None:
        report_path = Path(__file__).parent.parent / "reports" / "link_check_report.html"

    if not report_path.exists():
        print("❌ No report found. Run the test suite first.")
        return False

    content = report_path.read_text(encoding="utf-8")
    # Quick check: look for failure indicators in report
    if "❌" not in content:
        print("✅ Report exists and shows no failures.")
        return True

    # Count failures
    fail_count = content.count("❌")
    total_match = content.count("<tr>") - 1  # subtract header row
    if total_match > 0 and fail_count / total_match < 0.05:
        print(f"✅ Acceptable: {fail_count}/{total_match} links failed (<5%)")
        return True

    print(f"❌ Too many failures: {fail_count} links failed.")
    return False
