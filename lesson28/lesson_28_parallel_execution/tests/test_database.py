"""
Database operation tests with worker isolation.
Each worker gets its own database instance.
"""

import time
import json
import pytest


class TestDatabaseOperations:
    """Test database CRUD operations."""
    
    def test_create_user(self, worker_id, worker_database):
        """Test creating a user in the database."""
        print(f"[{worker_id}] Testing user creation in {worker_database}")
        time.sleep(1.2)
        
        # Read current database
        with open(worker_database, 'r') as f:
            db = json.load(f)
        
        # Add user
        db["users"].append({"id": 1, "name": "John"})
        
        # Write back
        with open(worker_database, 'w') as f:
            json.dump(db, f)
        
        assert len(db["users"]) == 1
    
    def test_create_product(self, worker_id, worker_database):
        """Test creating a product in the database."""
        print(f"[{worker_id}] Testing product creation in {worker_database}")
        time.sleep(1.2)
        
        with open(worker_database, 'r') as f:
            db = json.load(f)
        
        db["products"].append({"id": 1, "name": "Keyboard"})
        
        with open(worker_database, 'w') as f:
            json.dump(db, f)
        
        assert len(db["products"]) == 1
    
    def test_read_users(self, worker_id, worker_database):
        """Test reading users from the database."""
        print(f"[{worker_id}] Testing user read from {worker_database}")
        time.sleep(1.2)
        
        with open(worker_database, 'r') as f:
            db = json.load(f)
        
        # Database should be empty for this worker
        assert isinstance(db["users"], list)
    
    def test_read_products(self, worker_id, worker_database):
        """Test reading products from the database."""
        print(f"[{worker_id}] Testing product read from {worker_database}")
        time.sleep(1.2)
        
        with open(worker_database, 'r') as f:
            db = json.load(f)
        
        assert isinstance(db["products"], list)
