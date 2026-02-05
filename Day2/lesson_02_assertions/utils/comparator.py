"""Deep dictionary comparison utility for production test suites."""

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
        
        lines = [f"\nFound {len(self.differences)} difference(s):\n"]
        for diff in self.differences:
            lines.append(f"  [{diff.type}] {diff.path}")
            lines.append(f"    Expected: {repr(diff.expected)}")
            lines.append(f"    Actual:   {repr(diff.actual)}")
        return "\n".join(lines)


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
