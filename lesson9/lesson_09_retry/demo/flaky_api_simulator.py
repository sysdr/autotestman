"""
Flaky API Simulator - Simulates unreliable network calls for testing
"""

import random
import time
from typing import Optional


class FlakinesSimulator:
    """Simulates various failure modes common in production systems."""
    
    def __init__(self, failure_rate: float = 0.7):
        """
        Args:
            failure_rate: Probability of failure (0.0 to 1.0)
        """
        self.failure_rate = failure_rate
        self.call_count = 0
    
    def flaky_network_call(self, data: str = "test") -> dict:
        """
        Simulates a network call that fails randomly.
        
        Fails with ConnectionError ~70% of the time initially,
        but succeeds eventually (simulating transient failures).
        """
        self.call_count += 1
        
        # Simulate network latency
        time.sleep(random.uniform(0.05, 0.15))
        
        # Fail randomly based on failure_rate
        # But guarantee success after 3 attempts (realistic transient failure)
        if self.call_count < 3 and random.random() < self.failure_rate:
            raise ConnectionError(f"Connection timeout (attempt {self.call_count})")
        
        return {
            "status": "success",
            "data": data,
            "attempt": self.call_count
        }
    
    def flaky_database_query(self, query: str) -> list:
        """Simulates a database query that occasionally fails."""
        self.call_count += 1
        
        # Simulate query time
        time.sleep(random.uniform(0.02, 0.08))
        
        if self.call_count < 2 and random.random() < self.failure_rate:
            raise TimeoutError("Database connection pool exhausted")
        
        return [{"id": 1, "query": query, "attempt": self.call_count}]
    
    def always_fails(self) -> None:
        """Function that always fails - tests that retry gives up eventually."""
        self.call_count += 1
        raise RuntimeError(f"Persistent failure (attempt {self.call_count})")
    
    def reset(self):
        """Reset call counter."""
        self.call_count = 0
