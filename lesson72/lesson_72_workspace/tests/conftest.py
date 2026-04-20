# tests/conftest.py
# Shared pytest fixtures for the UQAP test suite.
# conftest.py is auto-discovered by pytest — no imports needed.

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture(scope="session")
def workspace_root() -> Path:
    """Returns the project root directory. Used by tests that need file paths."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def ci_environment() -> dict[str, str]:
    """
    Detects which CI system we're running inside (if any).
    Returns a dict of CI metadata — useful for conditional test logic.
    
    Production pattern: Never hard-code CI environment assumptions.
    Detect and adapt at runtime.
    """
    import os
    return {
        "is_jenkins": os.environ.get("JENKINS_URL", "") != "",
        "is_github_actions": os.environ.get("GITHUB_ACTIONS", "") == "true",
        "is_local": not (
            os.environ.get("CI", "") or os.environ.get("JENKINS_URL", "")
        ),
        "python_version": f"{__import__('sys').version_info.major}.{__import__('sys').version_info.minor}",
        "build_number": os.environ.get("BUILD_NUMBER", "local"),
        "commit_sha": os.environ.get("GITHUB_SHA", os.environ.get("GIT_COMMIT", "unknown")),
    }


@pytest.fixture(autouse=True)
def log_test_timing(request: pytest.FixtureRequest) -> Generator[None, None, None]:
    """
    Auto-applied fixture: logs start/end time for every test.
    'autouse=True' means every test gets this without asking for it.
    'yield' is the test body — code before yield is setup, after is teardown.
    """
    start = time.perf_counter()
    yield  # ← test runs here
    duration = time.perf_counter() - start
    
    # In production: send to metrics system (Datadog, Prometheus, etc.)
    if duration > 2.0:
        print(f"\n⚠️  SLOW TEST: {request.node.name} took {duration:.2f}s (threshold: 2.0s)")
