"""Test cases for DictComparator."""

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
