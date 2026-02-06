"""
Data Validation Tests
Demonstrates PyTest assertions, fixtures, and test isolation.
"""

import json
import pytest
from pathlib import Path


def test_user_emails_are_valid(data_file):
    """
    Validates that all user emails contain '@' symbol.
    Uses data_file fixture for isolated test data.
    """
    with open(data_file) as f:
        data = json.load(f)
    
    for user in data['users']:
        assert '@' in user['email'], (
            f"Invalid email format for user '{user['name']}': {user['email']}"
        )


def test_user_ids_are_unique(data_file):
    """
    Validates that user IDs are unique across all users.
    Demonstrates list comprehension and set comparison.
    """
    with open(data_file) as f:
        data = json.load(f)
    
    user_ids = [user['id'] for user in data['users']]
    unique_ids = set(user_ids)
    
    assert len(user_ids) == len(unique_ids), (
        f"Duplicate user IDs detected. "
        f"Total: {len(user_ids)}, Unique: {len(unique_ids)}, IDs: {user_ids}"
    )


def test_config_has_required_fields(data_file):
    """
    Validates configuration structure has all required fields.
    Shows multiple assertions in a single test.
    """
    with open(data_file) as f:
        data = json.load(f)
    
    config = data['config']
    
    # Check field existence
    required_fields = ['timeout', 'max_retries', 'api_base_url']
    for field in required_fields:
        assert field in config, f"Missing required config field: '{field}'"
    
    # Check field types
    assert isinstance(config['timeout'], int), (
        f"'timeout' must be integer, got {type(config['timeout']).__name__}"
    )
    assert isinstance(config['max_retries'], int), (
        f"'max_retries' must be integer, got {type(config['max_retries']).__name__}"
    )
    assert isinstance(config['api_base_url'], str), (
        f"'api_base_url' must be string, got {type(config['api_base_url']).__name__}"
    )


def test_active_users_count(data_file):
    """
    Counts active vs inactive users.
    Demonstrates filtering and counting patterns.
    """
    with open(data_file) as f:
        data = json.load(f)
    
    active_users = [u for u in data['users'] if u.get('active', False)]
    inactive_users = [u for u in data['users'] if not u.get('active', False)]
    
    assert len(active_users) > 0, "Expected at least one active user"
    assert len(active_users) + len(inactive_users) == len(data['users']), (
        f"User count mismatch: {len(active_users)} active + "
        f"{len(inactive_users)} inactive != {len(data['users'])} total"
    )
