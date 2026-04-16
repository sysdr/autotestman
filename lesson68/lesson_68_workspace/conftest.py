"""
conftest.py — UQAP Lesson 68: BDD Reporting Hooks

This file is the heart of the reporting system.
It uses the Observer/Hook pattern to collect scenario results
WITHOUT modifying any test code.

Key hooks used:
  - pytest_runtest_makereport : captures pass/fail per test item
  - pytest_sessionstart       : records session start time
  - pytest_sessionfinish      : triggers HTML report generation
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path
from datetime import datetime

import pytest


# ─── Data Model ───────────────────────────────────────────────────────────────

@dataclass
class ScenarioResult:
    feature: str
    scenario: str
    status: str          # "PASSED" | "FAILED" | "ERROR"
    duration_ms: float
    timestamp: str
    error: str | None = None
    steps: list[str] = field(default_factory=list)


# ─── Session-level State (module-level, reset per session) ────────────────────

_results: list[ScenarioResult] = []
_session_start: float = 0.0
_item_start_times: dict[str, float] = {}


# ─── Hooks ────────────────────────────────────────────────────────────────────

def pytest_sessionstart(session: pytest.Session) -> None:
    global _session_start, _results, _item_start_times
    _session_start = time.perf_counter()
    _results = []
    _item_start_times = {}


def pytest_runtest_setup(item: pytest.Item) -> None:
    _item_start_times[item.nodeid] = time.perf_counter()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> None:
    """
    Wraps pytest's own report generation.
    The `yield` is mandatory — it lets pytest create the report first,
    then we read the result.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return  # Ignore setup/teardown phases

    start = _item_start_times.get(item.nodeid, time.perf_counter())
    duration_ms = (time.perf_counter() - start) * 1000

    # Extract BDD metadata injected by pytest-bdd
    scenario = getattr(item, '_scenario', None)
    feature  = getattr(item, '_feature',  None)

    scenario_name = scenario.name if scenario else item.name
    feature_name  = feature.name  if feature  else "Unknown Feature"

    error_text: str | None = None
    if report.failed:
        error_text = str(report.longrepr)
        # Trim to first 500 chars for readability in HTML
        if len(error_text) > 500:
            error_text = error_text[:497] + "..."

    _results.append(ScenarioResult(
        feature=feature_name,
        scenario=scenario_name,
        status="PASSED" if report.passed else "FAILED",
        duration_ms=round(duration_ms, 2),
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        error=error_text,
    ))


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    from utils.bdd_reporter import generate_html_report

    session_duration_s = time.perf_counter() - _session_start
    report_path = Path("reports") / "cucumber_report.html"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    generate_html_report(
        results=_results,
        session_duration_s=session_duration_s,
        output_path=report_path,
    )
    print(f"\n📊 BDD Report → {report_path.resolve()}")
