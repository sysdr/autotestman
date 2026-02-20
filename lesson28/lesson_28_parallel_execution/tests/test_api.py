"""
API endpoint tests that can run in parallel.
Each test simulates an independent API call.
"""

import time
import pytest


class TestAPIEndpoints:
    """Test various API endpoints."""
    
    def test_get_users(self, worker_id, worker_port):
        """Test GET /users endpoint."""
        print(f"[{worker_id}] Testing GET /users on port {worker_port}")
        time.sleep(1.5)  # Simulate API latency
        
        # Simulate API response
        users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
        assert len(users) == 2
        assert users[0]["name"] == "Alice"
    
    def test_get_products(self, worker_id, worker_port):
        """Test GET /products endpoint."""
        print(f"[{worker_id}] Testing GET /products on port {worker_port}")
        time.sleep(1.5)
        
        products = [{"id": 1, "name": "Laptop"}, {"id": 2, "name": "Mouse"}]
        assert len(products) == 2
        assert products[0]["name"] == "Laptop"
    
    def test_get_orders(self, worker_id, worker_port):
        """Test GET /orders endpoint."""
        print(f"[{worker_id}] Testing GET /orders on port {worker_port}")
        time.sleep(1.5)
        
        orders = [{"id": 1, "status": "completed"}]
        assert len(orders) == 1
        assert orders[0]["status"] == "completed"
    
    def test_get_analytics(self, worker_id, worker_port):
        """Test GET /analytics endpoint."""
        print(f"[{worker_id}] Testing GET /analytics on port {worker_port}")
        time.sleep(1.5)
        
        analytics = {"total_users": 100, "total_orders": 50}
        assert analytics["total_users"] == 100
