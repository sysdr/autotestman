"""
Shared PyTest fixtures for all tests.
Fixtures defined here are automatically discovered by PyTest.
"""

import pytest
import tempfile
import json
from pathlib import Path
from typing import Dict, Any


@pytest.fixture
def temp_workspace():
    """
    Creates an isolated temporary directory for each test.
    Automatically cleaned up after test completes.
    
    Yield pattern ensures cleanup even if test fails.
    """
    workspace = tempfile.mkdtemp()
    workspace_path = Path(workspace)
    
    yield workspace_path
    
    # Cleanup after test
    import shutil
    shutil.rmtree(workspace, ignore_errors=True)


@pytest.fixture
def sample_data() -> Dict[str, Any]:
    """
    Provides consistent test data across all tests.
    Centralized data prevents hardcoding in test bodies.
    """
    return {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com", "active": True},
            {"id": 2, "name": "Bob", "email": "bob@example.com", "active": True},
            {"id": 3, "name": "Charlie", "email": "charlie@example.com", "active": False}
        ],
        "config": {
            "timeout": 30,
            "max_retries": 3,
            "api_base_url": "https://api.example.com"
        }
    }


@pytest.fixture
def data_file(temp_workspace, sample_data):
    """
    Fixture composition: depends on temp_workspace and sample_data.
    Creates a JSON file containing test data.
    """
    file_path = temp_workspace / "test_data.json"
    with open(file_path, 'w') as f:
        json.dump(sample_data, f, indent=2)
    return file_path
