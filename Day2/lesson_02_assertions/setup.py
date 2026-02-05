# setup_lesson.py
"""
Lesson 2: Deep Dictionary Comparison with Custom Assertions
Generates a complete workspace for learning production-grade assertion logic.
"""

import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any
import json
from datetime import datetime

# ============================================================================
# PHASE 1: DATA STRUCTURES
# ============================================================================

@dataclass
class Difference:
    """Represents a single mismatch between expected and actual values."""
    path: str
    expected: Any
    actual: Any
    type: str  # "missing_key", "extra_key", "value_mismatch", "type_mismatch"
    
    def to_dict(self) -> dict:
        return {
            "path": self.path,
            "expected": str(self.expected),
            "actual": str(self.actual),
            "type": self.type
        }


class DictMismatchError(AssertionError):
    """Custom exception for dictionary comparison failures with rich diagnostics."""
    
    def __init__(self, differences: list[Difference]):
        self.differences = differences
        report = self._format_report()
        super().__init__(report)
    
    def _format_report(self) -> str:
        """Generate a human-readable diff report."""
        if not self.differences:
            return "Dictionaries are identical."
        
        lines = [f"\n{'='*70}"]
        lines.append(f"DICTIONARY MISMATCH: Found {len(self.differences)} difference(s)")
        lines.append(f"{'='*70}\n")
        
        for i, diff in enumerate(self.differences, 1):
            lines.append(f"{i}. [{diff.type.upper()}] Path: {diff.path}")
            lines.append(f"   Expected: {repr(diff.expected)}")
            lines.append(f"   Actual:   {repr(diff.actual)}")
            lines.append("")
        
        return "\n".join(lines)


# ============================================================================
# PHASE 2: COMPARATOR ENGINE
# ============================================================================

class DictComparator:
    """
    Deep recursive dictionary comparator with exclusion rules.
    
    Usage:
        comparator = DictComparator(exclude_keys=["timestamp", "request_id"])
        comparator.assert_equal(expected, actual)
    """
    
    def __init__(self, exclude_keys: set[str] | None = None, tolerance: float = 0.0):
        self.exclude_keys = exclude_keys or set()
        self.tolerance = tolerance  # For floating point comparisons
        self.differences: list[Difference] = []
    
    def assert_equal(self, expected: dict, actual: dict) -> None:
        """
        Compare two dictionaries and raise DictMismatchError if they differ.
        
        Args:
            expected: The expected dictionary
            actual: The actual dictionary to compare
            
        Raises:
            DictMismatchError: If dictionaries don't match
        """
        self.differences = []  # Reset for new comparison
        self._compare_dicts(expected, actual, path="root")
        
        if self.differences:
            raise DictMismatchError(self.differences)
    
    def _compare_dicts(self, expected: dict, actual: dict, path: str) -> None:
        """Recursively compare two dictionaries."""
        # Find missing keys (in expected but not actual)
        for key in expected:
            if key in self.exclude_keys:
                continue
            if key not in actual:
                self.differences.append(
                    Difference(
                        path=f"{path}.{key}",
                        expected=expected[key],
                        actual="<missing>",
                        type="missing_key"
                    )
                )
        
        # Find extra keys (in actual but not expected)
        for key in actual:
            if key in self.exclude_keys:
                continue
            if key not in expected:
                self.differences.append(
                    Difference(
                        path=f"{path}.{key}",
                        expected="<missing>",
                        actual=actual[key],
                        type="extra_key"
                    )
                )
        
        # Compare shared keys
        for key in expected:
            if key not in actual or key in self.exclude_keys:
                continue
            
            exp_val = expected[key]
            act_val = actual[key]
            new_path = f"{path}.{key}"
            
            # Type mismatch
            if type(exp_val) != type(act_val):
                self.differences.append(
                    Difference(
                        path=new_path,
                        expected=f"{exp_val} (type: {type(exp_val).__name__})",
                        actual=f"{act_val} (type: {type(act_val).__name__})",
                        type="type_mismatch"
                    )
                )
                continue
            
            # Nested dictionary
            if isinstance(exp_val, dict):
                self._compare_dicts(exp_val, act_val, new_path)
            # List
            elif isinstance(exp_val, list):
                self._compare_lists(exp_val, act_val, new_path)
            # Numeric with tolerance
            elif isinstance(exp_val, (int, float)) and isinstance(act_val, (int, float)):
                if abs(exp_val - act_val) > self.tolerance:
                    self.differences.append(
                        Difference(
                            path=new_path,
                            expected=exp_val,
                            actual=act_val,
                            type="value_mismatch"
                        )
                    )
            # Direct value comparison
            elif exp_val != act_val:
                self.differences.append(
                    Difference(
                        path=new_path,
                        expected=exp_val,
                        actual=act_val,
                        type="value_mismatch"
                    )
                )
    
    def _compare_lists(self, expected: list, actual: list, path: str) -> None:
        """Compare two lists element by element."""
        if len(expected) != len(actual):
            self.differences.append(
                Difference(
                    path=f"{path}.length",
                    expected=len(expected),
                    actual=len(actual),
                    type="value_mismatch"
                )
            )
            # Continue comparing up to the shorter length
        
        for i in range(min(len(expected), len(actual))):
            exp_item = expected[i]
            act_item = actual[i]
            item_path = f"{path}[{i}]"
            
            if isinstance(exp_item, dict) and isinstance(act_item, dict):
                self._compare_dicts(exp_item, act_item, item_path)
            elif isinstance(exp_item, list) and isinstance(act_item, list):
                self._compare_lists(exp_item, act_item, item_path)
            elif exp_item != act_item:
                self.differences.append(
                    Difference(
                        path=item_path,
                        expected=exp_item,
                        actual=act_item,
                        type="value_mismatch"
                    )
                )


# ============================================================================
# PHASE 3: TEST CASES
# ============================================================================

def run_test_cases() -> dict[str, bool]:
    """Run all test scenarios and return results."""
    results = {}
    
    # Test 1: Identical dictionaries
    print("\n" + "="*70)
    print("TEST 1: Identical Dictionaries (Should PASS)")
    print("="*70)
    try:
        expected = {"name": "Alice", "age": 30, "active": True}
        actual = {"name": "Alice", "age": 30, "active": True}
        comparator = DictComparator()
        comparator.assert_equal(expected, actual)
        print("✅ PASSED: Dictionaries are identical")
        results["test_identical"] = True
    except DictMismatchError as e:
        print(f"❌ FAILED: {e}")
        results["test_identical"] = False
    
    # Test 2: Value mismatch
    print("\n" + "="*70)
    print("TEST 2: Value Mismatch (Should FAIL with diagnostics)")
    print("="*70)
    try:
        expected = {"name": "Alice", "age": 30}
        actual = {"name": "Alice", "age": 31}
        comparator = DictComparator()
        comparator.assert_equal(expected, actual)
        print("❌ FAILED: Should have caught mismatch")
        results["test_value_mismatch"] = False
    except DictMismatchError as e:
        print(f"✅ PASSED: Caught mismatch correctly\n{e}")
        results["test_value_mismatch"] = True
    
    # Test 3: Nested structure mismatch
    print("\n" + "="*70)
    print("TEST 3: Nested Structure Mismatch")
    print("="*70)
    try:
        expected = {
            "user": {
                "profile": {
                    "address": {"city": "NYC", "zip": "10001"}
                }
            }
        }
        actual = {
            "user": {
                "profile": {
                    "address": {"city": "LA", "zip": "90001"}
                }
            }
        }
        comparator = DictComparator()
        comparator.assert_equal(expected, actual)
        print("❌ FAILED: Should have caught nested mismatch")
        results["test_nested"] = False
    except DictMismatchError as e:
        print(f"✅ PASSED: Caught nested mismatch\n{e}")
        results["test_nested"] = True
    
    # Test 4: Exclude dynamic keys
    print("\n" + "="*70)
    print("TEST 4: Exclude Dynamic Keys (timestamps, IDs)")
    print("="*70)
    try:
        expected = {"data": [1, 2, 3], "status": "success"}
        actual = {
            "data": [1, 2, 3],
            "status": "success",
            "timestamp": "2026-02-04T10:30:00Z",
            "request_id": "abc123"
        }
        comparator = DictComparator(exclude_keys={"timestamp", "request_id"})
        comparator.assert_equal(expected, actual)
        print("✅ PASSED: Ignored excluded keys")
        results["test_exclude"] = True
    except DictMismatchError as e:
        print(f"❌ FAILED: Should have ignored excluded keys\n{e}")
        results["test_exclude"] = False
    
    # Test 5: Missing keys
    print("\n" + "="*70)
    print("TEST 5: Missing Required Keys")
    print("="*70)
    try:
        expected = {"name": "Alice", "email": "alice@example.com", "phone": "555-1234"}
        actual = {"name": "Alice", "email": "alice@example.com"}
        comparator = DictComparator()
        comparator.assert_equal(expected, actual)
        print("❌ FAILED: Should have caught missing key")
        results["test_missing"] = False
    except DictMismatchError as e:
        print(f"✅ PASSED: Caught missing key\n{e}")
        results["test_missing"] = True
    
    # Test 6: List comparison
    print("\n" + "="*70)
    print("TEST 6: List Element Mismatch")
    print("="*70)
    try:
        expected = {"items": [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}]}
        actual = {"items": [{"id": 1, "name": "A"}, {"id": 2, "name": "C"}]}
        comparator = DictComparator()
        comparator.assert_equal(expected, actual)
        print("❌ FAILED: Should have caught list item mismatch")
        results["test_list"] = False
    except DictMismatchError as e:
        print(f"✅ PASSED: Caught list mismatch\n{e}")
        results["test_list"] = True
    
    return results


# ============================================================================
# PHASE 4: HTML REPORT GENERATOR
# ============================================================================

def generate_html_report(results: dict[str, bool]) -> str:
    """Generate an HTML report of test results."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Dictionary Comparison Test Report</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        .summary {{ background: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0; }}
        .summary h2 {{ margin-top: 0; color: #2c3e50; }}
        .metric {{ display: inline-block; margin: 10px 20px 10px 0; }}
        .metric-value {{ font-size: 32px; font-weight: bold; color: #3498db; }}
        .metric-label {{ font-size: 14px; color: #7f8c8d; text-transform: uppercase; }}
        .test-case {{ background: #fff; border-left: 4px solid #95a5a6; padding: 15px; margin: 10px 0; border-radius: 4px; }}
        .test-case.passed {{ border-left-color: #27ae60; }}
        .test-case.failed {{ border-left-color: #e74c3c; }}
        .status {{ font-weight: bold; padding: 5px 10px; border-radius: 3px; display: inline-block; }}
        .status.passed {{ background: #27ae60; color: white; }}
        .status.failed {{ background: #e74c3c; color: white; }}
        .timestamp {{ color: #95a5a6; font-size: 14px; }}
        .sample-failure {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 20px; margin: 20px 0; border-radius: 4px; }}
        .sample-failure h3 {{ margin-top: 0; color: #856404; }}
        .diff-item {{ background: #f8f9fa; padding: 12px; margin: 10px 0; border-radius: 3px; font-family: 'Courier New', monospace; }}
        .diff-path {{ color: #e74c3c; font-weight: bold; }}
        .diff-expected {{ color: #27ae60; }}
        .diff-actual {{ color: #e74c3c; }}
        .metrics {{ display: flex; gap: 30px; margin-top: 15px; }}
        .metric-item {{ display: flex; flex-direction: column; }}
        .metric-value-small {{ font-size: 18px; font-weight: bold; color: #2c3e50; }}
        .metric-label-small {{ font-size: 12px; color: #7f8c8d; text-transform: uppercase; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🧪 Dictionary Comparison Test Report</h1>
        <p class="timestamp">Generated: {timestamp}</p>
        
        <div class="summary">
            <h2>Summary</h2>
            <div class="metric">
                <div class="metric-value">{passed}/{total}</div>
                <div class="metric-label">Tests Passed</div>
            </div>
            <div class="metric">
                <div class="metric-value">{(passed/total*100):.1f}%</div>
                <div class="metric-label">Success Rate</div>
            </div>
        </div>
        
        <h2>Test Results</h2>
"""
    
    for test_name, passed in results.items():
        status_class = "passed" if passed else "failed"
        status_text = "PASSED ✅" if passed else "FAILED ❌"
        html += f"""
        <div class="test-case {status_class}">
            <span class="status {status_class}">{status_text}</span>
            <strong>{test_name}</strong>
        </div>
"""
    
    # Add sample failure section
    html += """
        <h2>📎 Sample Failure (Simulated)</h2>
        <div class="sample-failure">
            <h3>Email Domain Mismatch Example</h3>
            <div class="diff-item">
                <div class="diff-path">[value_mismatch] root.user.email</div>
                <div class="diff-expected">Expected: alice@example.com</div>
                <div class="diff-actual">Actual:   alice@newdomain.com</div>
            </div>
            <div class="metrics">
                <div class="metric-item">
                    <div class="metric-value-small">42ms</div>
                    <div class="metric-label-small">Avg Comparison Time</div>
                    <div style="font-size: 11px; color: #95a5a6; margin-top: 2px;">(10k keys)</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value-small">2</div>
                    <div class="metric-label-small">Differences Collected</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
    return html


# ============================================================================
# PHASE 5: WORKSPACE GENERATOR
# ============================================================================

def create_workspace():
    """Generate the complete lesson workspace structure."""
    # When run from within lesson_02_assertions directory, use current directory
    base_dir = Path(".")
    base_dir.mkdir(exist_ok=True)
    
    # Create directory structure
    (base_dir / "tests").mkdir(exist_ok=True)
    (base_dir / "utils").mkdir(exist_ok=True)
    (base_dir / "output").mkdir(exist_ok=True)
    
    # Write comparator module (only if it doesn't exist)
    comparator_file = base_dir / "utils" / "comparator.py"
    if not comparator_file.exists():
        comparator_code = '''"""Deep dictionary comparison utility for production test suites."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Difference:
    """Represents a single mismatch between expected and actual values."""
    path: str
    expected: Any
    actual: Any
    type: str


class DictMismatchError(AssertionError):
    """Custom exception for dictionary comparison failures."""
    
    def __init__(self, differences: list[Difference]):
        self.differences = differences
        report = self._format_report()
        super().__init__(report)
    
    def _format_report(self) -> str:
        if not self.differences:
            return "Dictionaries are identical."
        
        lines = [f"\\nFound {len(self.differences)} difference(s):\\n"]
        for diff in self.differences:
            lines.append(f"  [{diff.type}] {diff.path}")
            lines.append(f"    Expected: {repr(diff.expected)}")
            lines.append(f"    Actual:   {repr(diff.actual)}")
        return "\\n".join(lines)


class DictComparator:
    """Deep recursive dictionary comparator with exclusion rules."""
    
    def __init__(self, exclude_keys: set[str] | None = None, tolerance: float = 0.0):
        self.exclude_keys = exclude_keys or set()
        self.tolerance = tolerance
        self.differences: list[Difference] = []
    
    def assert_equal(self, expected: dict, actual: dict) -> None:
        """Compare dictionaries and raise DictMismatchError if different."""
        self.differences = []
        self._compare_dicts(expected, actual, path="root")
        
        if self.differences:
            raise DictMismatchError(self.differences)
    
    def _compare_dicts(self, expected: dict, actual: dict, path: str) -> None:
        """Recursively compare two dictionaries."""
        for key in expected:
            if key in self.exclude_keys:
                continue
            if key not in actual:
                self.differences.append(
                    Difference(f"{path}.{key}", expected[key], "<missing>", "missing_key")
                )
        
        for key in actual:
            if key in self.exclude_keys:
                continue
            if key not in expected:
                self.differences.append(
                    Difference(f"{path}.{key}", "<missing>", actual[key], "extra_key")
                )
        
        for key in expected:
            if key not in actual or key in self.exclude_keys:
                continue
            
            exp_val = expected[key]
            act_val = actual[key]
            new_path = f"{path}.{key}"
            
            if type(exp_val) != type(act_val):
                self.differences.append(
                    Difference(new_path, type(exp_val).__name__, type(act_val).__name__, "type_mismatch")
                )
            elif isinstance(exp_val, dict):
                self._compare_dicts(exp_val, act_val, new_path)
            elif isinstance(exp_val, list):
                self._compare_lists(exp_val, act_val, new_path)
            elif isinstance(exp_val, (int, float)) and abs(exp_val - act_val) > self.tolerance:
                self.differences.append(
                    Difference(new_path, exp_val, act_val, "value_mismatch")
                )
            elif exp_val != act_val:
                self.differences.append(
                    Difference(new_path, exp_val, act_val, "value_mismatch")
                )
    
    def _compare_lists(self, expected: list, actual: list, path: str) -> None:
        """Compare two lists element by element."""
        if len(expected) != len(actual):
            self.differences.append(
                Difference(f"{path}.length", len(expected), len(actual), "value_mismatch")
            )
        
        for i in range(min(len(expected), len(actual))):
            item_path = f"{path}[{i}]"
            if isinstance(expected[i], dict) and isinstance(actual[i], dict):
                self._compare_dicts(expected[i], actual[i], item_path)
            elif expected[i] != actual[i]:
                self.differences.append(
                    Difference(item_path, expected[i], actual[i], "value_mismatch")
                )
'''
    (base_dir / "utils" / "comparator.py").write_text(comparator_code)
    (base_dir / "utils" / "__init__.py").write_text("")
    
    # Write pytest test file
    test_code = '''"""Test cases for DictComparator."""

import pytest
from utils.comparator import DictComparator, DictMismatchError


def test_identical_dicts():
    """Test that identical dictionaries pass."""
    expected = {"name": "Alice", "age": 30}
    actual = {"name": "Alice", "age": 30}
    comparator = DictComparator()
    comparator.assert_equal(expected, actual)  # Should not raise


def test_value_mismatch():
    """Test that value mismatches are caught."""
    expected = {"name": "Alice", "age": 30}
    actual = {"name": "Alice", "age": 31}
    comparator = DictComparator()
    
    with pytest.raises(DictMismatchError) as exc_info:
        comparator.assert_equal(expected, actual)
    
    assert len(exc_info.value.differences) == 1
    assert exc_info.value.differences[0].path == "root.age"


def test_nested_mismatch():
    """Test nested structure comparison."""
    expected = {"user": {"profile": {"city": "NYC"}}}
    actual = {"user": {"profile": {"city": "LA"}}}
    comparator = DictComparator()
    
    with pytest.raises(DictMismatchError) as exc_info:
        comparator.assert_equal(expected, actual)
    
    assert "root.user.profile.city" in str(exc_info.value)


def test_exclude_keys():
    """Test exclusion of dynamic keys."""
    expected = {"data": [1, 2, 3]}
    actual = {"data": [1, 2, 3], "timestamp": "2026-02-04", "request_id": "abc"}
    
    comparator = DictComparator(exclude_keys={"timestamp", "request_id"})
    comparator.assert_equal(expected, actual)  # Should pass


def test_missing_keys():
    """Test detection of missing keys."""
    expected = {"name": "Alice", "email": "alice@example.com"}
    actual = {"name": "Alice"}
    comparator = DictComparator()
    
    with pytest.raises(DictMismatchError) as exc_info:
        comparator.assert_equal(expected, actual)
    
    assert any(d.type == "missing_key" for d in exc_info.value.differences)
'''
    (base_dir / "tests" / "test_comparator.py").write_text(test_code)
    (base_dir / "tests" / "__init__.py").write_text("")
    
    # Write README (only if it doesn't exist)
    readme_file = base_dir / "README.md"
    if not readme_file.exists():
        readme = '''# Lesson 2: Deep Dictionary Comparison

## Setup
```bash
pip install pytest
```

## Run Tests
```bash
pytest tests/test_comparator.py -v
```

## Run Interactive Demo
```bash
python setup.py
```

## Key Learnings
1. Never use `assert dict1 == dict2` in production
2. Always collect ALL differences, not just the first
3. Maintain path breadcrumbs for nested structures
4. Allow exclusion rules for dynamic fields
5. Raise custom exceptions with rich diagnostics
'''
        readme_file.write_text(readme)
    
    print(f"✅ Workspace created at: {base_dir.absolute()}")
    return base_dir


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main entry point."""
    print("\n" + "="*70)
    print("LESSON 2: DEEP DICTIONARY COMPARISON")
    print("Production-Grade Assertion Logic for Test Automation")
    print("="*70)
    
    # Create workspace
    workspace = create_workspace()
    
    # Run test cases
    results = run_test_cases()
    
    # Generate HTML report
    html_report = generate_html_report(results)
    report_path = workspace / "output" / "comparison_report.html"
    report_path.write_text(html_report, encoding='utf-8')
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    print(f"Tests Passed: {passed}/{total} ({passed/total*100:.1f}%)")
    print(f"\n📊 HTML Report: {report_path.absolute()}")
    print(f"📁 Workspace: {workspace.absolute()}")
    print("\nNext Steps:")
    print("  pytest tests/test_comparator.py -v")
    print("="*70)


if __name__ == "__main__":
    main()