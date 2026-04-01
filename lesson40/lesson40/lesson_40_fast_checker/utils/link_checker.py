# utils/link_checker.py
"""
Core link-checking engine.
Pattern: Fan-Out / Fan-In using asyncio.gather()

Key design decisions:
1. APIRequestContext over page.goto() — 10x faster, no DOM overhead.
2. asyncio.gather(return_exceptions=True) — one timeout doesn't kill the run.
3. Dataclass result model — typed, serializable, no magic dicts.
4. Concurrency cap (semaphore) — prevents OS socket exhaustion on large sites.
"""

import asyncio
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence
from playwright.async_api import APIRequestContext, Page

MAX_CONCURRENT = 20  # Tune based on target server tolerance


@dataclass
class LinkResult:
    url: str
    status: int
    ok: bool
    error: str = ""
    elapsed_ms: float = 0.0


@dataclass
class CheckReport:
    target_url: str
    total: int = 0
    passed: int = 0
    failed: int = 0
    execution_time_s: float = 0.0
    results: list[LinkResult] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        return (self.passed / self.total * 100) if self.total > 0 else 0.0

    @property
    def all_passed(self) -> bool:
        return self.failed == 0 and self.total > 0


async def _check_single_link(
    context: APIRequestContext,
    url: str,
    semaphore: asyncio.Semaphore,
) -> LinkResult:
    """
    Check one URL. The semaphore limits how many run concurrently.
    This is the coroutine that gets fanned-out by asyncio.gather().
    """
    async with semaphore:
        start = asyncio.get_event_loop().time()
        try:
            response = await context.get(
                url,
                timeout=10_000,         # 10 second per-link timeout
                fail_on_status_code=False,  # Don't raise on 4xx/5xx
            )
            elapsed = (asyncio.get_event_loop().time() - start) * 1000
            return LinkResult(
                url=url,
                status=response.status,
                ok=response.ok,
                elapsed_ms=round(elapsed, 1),
            )
        except Exception as exc:
            elapsed = (asyncio.get_event_loop().time() - start) * 1000
            return LinkResult(
                url=url,
                status=0,
                ok=False,
                error=str(exc)[:120],
                elapsed_ms=round(elapsed, 1),
            )


def _extract_links(page_content: str, base_url: str) -> list[str]:
    """
    Extract all href values from raw HTML.
    Filters: absolute http/https only, deduplicates, excludes mailto/tel/anchor.
    """
    pattern = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)
    raw = pattern.findall(page_content)

    seen: set[str] = set()
    urls: list[str] = []

    for href in raw:
        href = href.strip()
        # Skip fragments, mailto, tel, javascript
        if href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue
        # Resolve relative paths to absolute
        if href.startswith("/"):
            # Extract scheme + host from base_url
            from urllib.parse import urlparse
            parsed = urlparse(base_url)
            href = f"{parsed.scheme}://{parsed.netloc}{href}"
        # Only check http/https
        if not href.startswith(("http://", "https://")):
            continue
        if href not in seen:
            seen.add(href)
            urls.append(href)

    return urls


async def run_fast_check(
    context: APIRequestContext,
    target_url: str,
) -> CheckReport:
    """
    Main entry point.
    1. Fetch homepage HTML via APIRequestContext (no browser needed for scraping)
    2. Extract all unique absolute links
    3. Fan-Out: dispatch all checks as coroutines
    4. Fan-In: await asyncio.gather() with a semaphore cap
    5. Return structured CheckReport
    """
    report = CheckReport(target_url=target_url)
    start_wall = asyncio.get_event_loop().time()

    # Step 1: Fetch homepage to extract links
    homepage_response = await context.get(target_url, timeout=15_000)
    html_content = await homepage_response.text()

    # Step 2: Extract links
    urls = _extract_links(html_content, target_url)
    report.total = len(urls)

    if not urls:
        return report

    # Step 3 & 4: Fan-Out / Fan-In
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    tasks = [_check_single_link(context, url, semaphore) for url in urls]

    # return_exceptions=True: one failure doesn't abort the gather
    raw_results = await asyncio.gather(*tasks, return_exceptions=True)

    # Step 5: Aggregate
    for item in raw_results:
        if isinstance(item, Exception):
            result = LinkResult(url="unknown", status=0, ok=False, error=str(item))
        else:
            result = item  # type: LinkResult
        report.results.append(result)
        if result.ok:
            report.passed += 1
        else:
            report.failed += 1

    report.execution_time_s = round(asyncio.get_event_loop().time() - start_wall, 2)
    return report


def generate_html_report(report: CheckReport, output_path: Path) -> None:
    """Generate a human-readable HTML report of the link check results."""
    rows = ""
    for r in sorted(report.results, key=lambda x: (x.ok, x.status)):
        status_color = "#22c55e" if r.ok else "#ef4444"
        icon = "✅" if r.ok else "❌"
        error_cell = f'<span style="color:#ef4444;font-size:0.8em">{r.error}</span>' if r.error else ""
        rows += f"""
        <tr>
            <td>{icon}</td>
            <td style="word-break:break-all"><a href="{r.url}" target="_blank">{r.url[:80]}{"..." if len(r.url)>80 else ""}</a></td>
            <td style="color:{status_color};font-weight:bold">{r.status or "ERR"}</td>
            <td>{r.elapsed_ms} ms</td>
            <td>{error_cell}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Fast Checker Report — {report.target_url}</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 2rem; background: #f8fafc; color: #1e293b; }}
  h1 {{ color: #1e40af; }}
  .summary {{ display: flex; gap: 2rem; margin: 1.5rem 0; }}
  .card {{ background: white; border-radius: 8px; padding: 1rem 2rem; box-shadow: 0 1px 3px rgba(0,0,0,.1); }}
  .card .val {{ font-size: 2rem; font-weight: bold; }}
  .pass {{ color: #16a34a; }} .fail {{ color: #dc2626; }} .info {{ color: #2563eb; }}
  table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,.1); }}
  th {{ background: #1e40af; color: white; padding: .75rem 1rem; text-align: left; }}
  td {{ padding: .6rem 1rem; border-bottom: 1px solid #e2e8f0; font-size: .9rem; }}
  tr:hover {{ background: #f1f5f9; }}
  .meta {{ font-size: .85rem; color: #64748b; margin-bottom: 1rem; }}
</style>
</head>
<body>
<h1>🔗 Fast Checker Report</h1>
<p class="meta">Target: <strong>{report.target_url}</strong> &nbsp;|&nbsp; Execution time: <strong>{report.execution_time_s}s</strong></p>
<div class="summary">
  <div class="card"><div class="val info">{report.total}</div><div>Total Links</div></div>
  <div class="card"><div class="val pass">{report.passed}</div><div>Passed (2xx)</div></div>
  <div class="card"><div class="val fail">{report.failed}</div><div>Failed</div></div>
  <div class="card"><div class="val {"pass" if report.success_rate==100 else "fail"}">{report.success_rate:.1f}%</div><div>Success Rate</div></div>
</div>
<table>
<thead><tr><th></th><th>URL</th><th>Status</th><th>Latency</th><th>Error</th></tr></thead>
<tbody>{rows}</tbody>
</table>
</body></html>"""

    output_path.write_text(html, encoding="utf-8")
