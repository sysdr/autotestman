"""
Basic Retry Decorator Tests
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.retry_decorator import retry, reset_retry_metrics
from demo.flaky_api_simulator import FlakinesSimulator


class TestRetryBasics:
    """Test basic retry decorator functionality."""
    
    def setup_method(self):
        """Reset metrics before each test."""
        reset_retry_metrics()
    
    def test_successful_function_no_retry(self):
        """Test that successful functions don't trigger retries."""
        call_count = 0
        
        @retry(attempts=3, delay=0.1)
        def always_succeeds():
            nonlocal call_count
            call_count += 1
            return "success"
        
        result = always_succeeds()
        
        assert result == "success"
        assert call_count == 1  # Called only once
    
    def test_flaky_function_succeeds_after_retry(self):
        """Test that flaky functions succeed after retry."""
        simulator = FlakinesSimulator(failure_rate=0.8)
        
        @retry(attempts=3, delay=0.1, exceptions=(ConnectionError,))
        def flaky_call():
            return simulator.flaky_network_call("test_data")
        
        result = flaky_call()
        
        assert result["status"] == "success"
        assert result["attempt"] > 1  # Required at least one retry
    
    def test_retry_gives_up_after_max_attempts(self):
        """Test that retry stops after maximum attempts."""
        simulator = FlakinesSimulator()
        
        @retry(attempts=3, delay=0.05, exceptions=(RuntimeError,))
        def always_fails():
            return simulator.always_fails()
        
        with pytest.raises(RuntimeError, match="Persistent failure"):
            always_fails()
        
        assert simulator.call_count == 3  # Tried exactly 3 times
    
    def test_exponential_backoff(self):
        """Test that delays increase exponentially."""
        import time
        
        attempt_times = []
        
        @retry(attempts=3, delay=0.1, backoff=2.0, exceptions=(ValueError,))
        def track_timing():
            attempt_times.append(time.time())
            if len(attempt_times) < 3:
                raise ValueError("Not yet")
            return "done"
        
        result = track_timing()
        
        assert result == "done"
        assert len(attempt_times) == 3
        
        # Check delays are approximately: 0.1s, 0.2s
        delay_1 = attempt_times[1] - attempt_times[0]
        delay_2 = attempt_times[2] - attempt_times[1]
        
        assert 0.08 < delay_1 < 0.15  # ~0.1s with tolerance
        assert 0.18 < delay_2 < 0.25  # ~0.2s with tolerance
    
    def test_specific_exception_filtering(self):
        """Test that only specified exceptions are retried."""
        call_count = 0
        
        @retry(attempts=3, delay=0.05, exceptions=(ConnectionError,))
        def raises_wrong_exception():
            nonlocal call_count
            call_count += 1
            raise ValueError("This should not be retried")
        
        with pytest.raises(ValueError, match="should not be retried"):
            raises_wrong_exception()
        
        assert call_count == 1  # Only called once, no retry
    
    def test_function_preserves_name(self):
        """Test that decorator preserves function metadata."""
        @retry(attempts=2)
        def my_function():
            """My docstring."""
            pass
        
        assert my_function.__name__ == "my_function"
        assert my_function.__doc__ == "My docstring."
