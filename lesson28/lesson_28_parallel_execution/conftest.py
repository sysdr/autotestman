"""
Fixtures for parallel test execution.
Each worker gets isolated resources to prevent conflicts.
"""

import pytest
from pathlib import Path
import json


@pytest.fixture(scope="session")
def worker_id(request):
    """Get the worker ID for this test session."""
    worker_id = getattr(request.config, "workerinput", {}).get("workerid", "master")
    return worker_id


@pytest.fixture(scope="session")
def worker_temp_dir(worker_id, tmp_path_factory):
    """Create a unique temp directory for this worker."""
    base_temp = tmp_path_factory.getbasetemp()
    worker_dir = base_temp / f"worker_{worker_id}"
    worker_dir.mkdir(exist_ok=True)
    return worker_dir


@pytest.fixture(scope="session")
def worker_port(worker_id):
    """Assign a unique port to each worker."""
    if worker_id == "master":
        return 8000
    
    # Extract worker number from "gw0", "gw1", etc.
    worker_num = int(worker_id.replace("gw", ""))
    return 8000 + worker_num + 1


@pytest.fixture(scope="session")
def worker_database(worker_id):
    """Simulate a unique database for each worker."""
    db_name = f"test_db_{worker_id}"
    
    # In a real scenario, you'd create an actual database here
    # For demo purposes, we'll use a JSON file
    db_file = Path(f"fixtures/{db_name}.json")
    db_file.parent.mkdir(exist_ok=True)
    
    # Initialize database
    db_file.write_text(json.dumps({"users": [], "products": []}))
    
    yield str(db_file)
    
    # Cleanup
    if db_file.exists():
        db_file.unlink()


@pytest.fixture
def isolated_counter(worker_temp_dir):
    """Each worker maintains its own counter."""
    counter_file = worker_temp_dir / "counter.txt"
    
    if not counter_file.exists():
        counter_file.write_text("0")
    
    def increment():
        current = int(counter_file.read_text())
        current += 1
        counter_file.write_text(str(current))
        return current
    
    return increment
