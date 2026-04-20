# tests/test_pipeline_config.py
# Lesson 72 Core Tests: Validate that CI configuration files are correct.
#
# Production insight: Test your CI config files themselves.
# A broken Jenkinsfile discovered at push time costs 5 minutes.
# Discovered in production costs 5 hours.

from __future__ import annotations

import re
from pathlib import Path

import pytest


# ─── Fixtures ─────────────────────────────────────────────────────────────────
@pytest.fixture(scope="module")
def project_root() -> Path:
    """Resolve project root relative to this test file."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="module")
def jenkinsfile(project_root: Path) -> str:
    """Load Jenkinsfile content for inspection."""
    jf = project_root / "Jenkinsfile"
    if not jf.exists():
        pytest.skip("Jenkinsfile not found — skipping Jenkins-specific tests")
    return jf.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def gha_workflow(project_root: Path) -> str:
    """Load GitHub Actions workflow YAML."""
    gha = project_root / ".github" / "workflows" / "tests.yml"
    if not gha.exists():
        pytest.skip("GitHub Actions workflow not found")
    return gha.read_text(encoding="utf-8")


# ─── Jenkinsfile Tests ─────────────────────────────────────────────────────────
class TestJenkinsfile:
    """
    Validate the structure and content of the Jenkinsfile.
    These tests enforce CI/CD best practices at the code level.
    """

    def test_jenkinsfile_uses_declarative_syntax(self, jenkinsfile: str) -> None:
        """Declarative pipelines are more readable and have better tooling than Scripted."""
        assert "pipeline {" in jenkinsfile, (
            "Must use declarative pipeline syntax: 'pipeline { ... }'"
        )

    def test_jenkinsfile_has_timeout_option(self, jenkinsfile: str) -> None:
        """
        Pipelines without timeouts can hang forever, consuming agent resources.
        Production rule: Every pipeline MUST have a timeout.
        """
        assert "timeout" in jenkinsfile, (
            "Jenkinsfile must define a timeout option to prevent hung builds."
        )

    def test_jenkinsfile_has_post_always_block(self, jenkinsfile: str) -> None:
        """
        'post { always { ... } }' ensures test reports are collected even when tests fail.
        Without this, a failed build gives you no diagnostic information.
        """
        assert "post" in jenkinsfile, "Jenkinsfile must have a post block"
        assert "always" in jenkinsfile, (
            "post block must include 'always' to collect artifacts on failure"
        )

    def test_jenkinsfile_publishes_junit_results(self, jenkinsfile: str) -> None:
        """Jenkins cannot render test trends without JUnit XML ingestion."""
        assert "junit" in jenkinsfile, (
            "Jenkinsfile must use 'junit' step to publish test results to Jenkins dashboard"
        )

    def test_jenkinsfile_uses_isolated_venv(self, jenkinsfile: str) -> None:
        """
        Never install packages globally on a Jenkins agent.
        Venv isolation prevents dependency bleeding between jobs.
        """
        assert "venv" in jenkinsfile, (
            "Tests must run inside a virtual environment, not global Python"
        )

    def test_jenkinsfile_has_build_discarder(self, jenkinsfile: str) -> None:
        """Retaining infinite builds fills disk. Enforce rotation policy."""
        assert "buildDiscarder" in jenkinsfile or "logRotator" in jenkinsfile, (
            "Set buildDiscarder to prevent disk exhaustion on Jenkins agents"
        )

    def test_jenkinsfile_exports_junitxml(self, jenkinsfile: str) -> None:
        """Pytest must output JUnit XML for Jenkins to parse."""
        assert "--junitxml" in jenkinsfile, (
            "pytest must be called with --junitxml flag to generate parseable reports"
        )


# ─── GitHub Actions Tests ─────────────────────────────────────────────────────
class TestGitHubActions:
    """Validate the GitHub Actions workflow configuration."""

    def test_workflow_triggers_on_push(self, gha_workflow: str) -> None:
        """CI must trigger automatically on push — no manual intervention."""
        assert "push:" in gha_workflow, (
            "Workflow must trigger on push events"
        )

    def test_workflow_triggers_on_pull_request(self, gha_workflow: str) -> None:
        """PRs without automated tests are a code review antipattern."""
        assert "pull_request:" in gha_workflow, (
            "Workflow must trigger on pull_request to catch bugs before merge"
        )

    def test_workflow_pins_python_version(self, gha_workflow: str) -> None:
        """
        'python-version: 3.x' without pinning causes random upgrades mid-project.
        Pin to a specific minor version for reproducibility.
        """
        assert "python-version" in gha_workflow, (
            "Workflow must explicitly set Python version via setup-python action"
        )
        # Ensure it's a real version string, not a wildcard
        assert re.search(r'python-version.*3[.]\d+', gha_workflow), (
            "Python version must be pinned to a specific minor version (e.g., '3.11')"
        )

    def test_workflow_uses_pip_cache(self, gha_workflow: str) -> None:
        """
        Without pip caching, every run re-downloads all packages.
        On a slow network: 2 extra minutes per run × 40 runs/day = 80 wasted minutes.
        """
        assert 'cache: "pip"' in gha_workflow or "cache: pip" in gha_workflow, (
            "Enable pip caching in setup-python action to speed up CI runs"
        )

    def test_workflow_uploads_artifacts_on_failure(self, gha_workflow: str) -> None:
        """Test reports must be preserved even when the job fails."""
        assert "if: always()" in gha_workflow, (
            "Artifact upload step must use 'if: always()' to preserve reports on failure"
        )

    def test_workflow_sets_retention_days(self, gha_workflow: str) -> None:
        """GitHub Actions deletes artifacts after 90 days by default. Be explicit."""
        assert "retention-days" in gha_workflow, (
            "Set explicit retention-days to control artifact storage lifecycle"
        )


# ─── Requirements Tests ───────────────────────────────────────────────────────
class TestRequirements:
    """Enforce pinned dependency discipline."""

    def test_requirements_file_exists(self, project_root: Path) -> None:
        req = project_root / "requirements.txt"
        assert req.exists(), "requirements.txt must exist for hermetic CI builds"

    def test_requirements_are_pinned(self, project_root: Path) -> None:
        """
        '>=' means 'install any version equal to or newer'. In CI, this means:
        Today: selenium==4.18.1 (works)
        Next month: selenium==4.19.0 (breaks your tests, you don't know why)
        
        Pin everything with '=='.
        """
        req_text = (project_root / "requirements.txt").read_text()
        lines = [
            line.strip() for line in req_text.splitlines()
            if line.strip() and not line.startswith("#")
        ]
        for line in lines:
            assert ">=" not in line and "~=" not in line, (
                f"Dependency '{line}' must be pinned with == not >= or ~= for reproducible builds"
            )
            assert "==" in line, (
                f"Dependency '{line}' must be pinned with == (e.g., 'pytest==8.3.2')"
            )
