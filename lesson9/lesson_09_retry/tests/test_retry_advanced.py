"""
Advanced Retry Decorator Tests - Real-world scenarios
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.retry_decorator import retry, get_retry_metrics, reset_retry_metrics
from demo.flaky_api_simulator import FlakinesSimulator


class TestRetryAdvanced:
    """Test advanced retry scenarios and metrics."""
    
    def setup_method(self):
        """Reset metrics before each test."""
        reset_retry_metrics()
    
    def test_retry_with_arguments(self):
        """Test retry decorator works with function arguments."""
        simulator = FlakinesSimulator(failure_rate=0.7)
        
        @retry(attempts=3, delay=0.05, exceptions=(ConnectionError,))
        def fetch_user_data(user_id: int, format: str = "json"):
            result = simulator.flaky_network_call(f"user_{user_id}")
            result["format"] = format
            return result
        
        result = fetch_user_data(42, format="xml")
        
        assert "user_42" in result["data"]
        assert result["format"] == "xml"
    
    def test_retry_metrics_tracking(self):
        """Test that metrics are tracked correctly."""
        reset_retry_metrics()
        
        simulator1 = FlakinesSimulator(failure_rate=1.0)
        simulator2 = FlakinesSimulator(failure_rate=0)
        
        @retry(attempts=3, delay=0.05, exceptions=(ConnectionError,))
        def flaky_call():
            return simulator1.flaky_network_call()
        
        @retry(attempts=3, delay=0.05)
        def stable_call():
            return simulator2.flaky_network_call()
        
        # Make some calls
        flaky_call()  # Will need retry
        stable_call()  # Won't need retry
        stable_call()  # Won't need retry
        
        metrics = get_retry_metrics()
        
        assert metrics["total_calls"] == 3
        assert float(metrics["retry_rate"].rstrip("%")) > 0  # At least one retry
    
    def test_database_retry_scenario(self):
        """Test retry with database-like operations."""
        simulator = FlakinesSimulator(failure_rate=0.6)
        
        @retry(attempts=3, delay=0.05, exceptions=(TimeoutError,))
        def execute_query(sql: str):
            return simulator.flaky_database_query(sql)
        
        result = execute_query("SELECT * FROM users")
        
        assert isinstance(result, list)
        assert len(result) > 0
    
    def test_multiple_exception_types(self):
        """Test retrying on multiple exception types."""
        call_count = 0
        
        @retry(attempts=4, delay=0.05, exceptions=(ConnectionError, TimeoutError, ValueError))
        def raises_different_exceptions():
            nonlocal call_count
            call_count += 1
            
            if call_count == 1:
                raise ConnectionError("Network error")
            elif call_count == 2:
                raise TimeoutError("Timeout")
            elif call_count == 3:
                raise ValueError("Validation error")
            else:
                return "finally succeeded"
        
        result = raises_different_exceptions()
        
        assert result == "finally succeeded"
        assert call_count == 4
    
    def test_no_retry_on_assertion_error(self):
        """Test that assertion errors are NOT retried (real bugs)."""
        call_count = 0
        
        @retry(attempts=3, delay=0.05, exceptions=(ConnectionError,))
        def test_with_assertion():
            nonlocal call_count
            call_count += 1
            result = {"value": 10}
            assert result["value"] == 20, "Value should be 20"
        
        with pytest.raises(AssertionError, match="Value should be 20"):
            test_with_assertion()
        
        assert call_count == 1  # Should NOT retry assertion failures
