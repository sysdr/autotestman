# tests/test_sanity.py
# Fast sanity checks that run in < 1 second.
# These are the "canary" tests — if these fail, something is very wrong
# with the environment, not the application under test.

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest


def test_python_version_is_supported() -> None:
    """
    Python 3.10 and earlier lack structural pattern matching and newer typing features.
    Enforce minimum version at the test level, not just in documentation.
    """
    major, minor = sys.version_info.major, sys.version_info.minor
    assert (major, minor) >= (3, 11), (
        f"UQAP requires Python 3.11+. Found: {major}.{minor}. "
        f"Update your runtime or CI agent image."
    )


def test_required_packages_importable() -> None:
    """
    Fail fast if packages are missing.
    Clearer than 'ModuleNotFoundError' buried in a 500-line log.
    """
    required = ["pytest"]
    missing = []
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)

    assert not missing, (
        f"Required packages not installed: {missing}. "
        f"Run: pip install -r requirements.txt"
    )


def test_ci_environment_detected(ci_environment: dict) -> None:
    """
    Validates our CI detection fixture returns the expected shape.
    Tests the test infrastructure itself — meta, but important.
    """
    expected_keys = {"is_jenkins", "is_github_actions", "is_local", 
                     "python_version", "build_number", "commit_sha"}
    actual_keys = set(ci_environment.keys())
    assert actual_keys == expected_keys, (
        f"CI environment dict missing keys: {expected_keys - actual_keys}"
    )


def test_reports_directory_is_writable(tmp_path: Path) -> None:
    """
    Jenkins/GHA must be able to write test reports.
    A read-only filesystem would silently swallow all test output.
    """
    test_file = tmp_path / "probe.txt"
    test_file.write_text("write_check")
    assert test_file.read_text() == "write_check"


@pytest.mark.parametrize("var,expected", [
    ("PYTHONUNBUFFERED", "1"),    # set in Jenkinsfile environment block
])
def test_ci_environment_variables_set(var: str, expected: str, ci_environment: dict) -> None:
    """
    Verify environment variables declared in Jenkinsfile are actually present.
    Only validated when running inside Jenkins (not locally).
    """
    if not ci_environment["is_jenkins"]:
        pytest.skip("This test only validates Jenkins environment configuration")
    assert os.environ.get(var) == expected, (
        f"Jenkins environment variable {var} should be '{expected}', "
        f"got: '{os.environ.get(var)}'. Check your Jenkinsfile 'environment' block."
    )
