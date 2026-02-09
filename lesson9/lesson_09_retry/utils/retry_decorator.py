"""
Retry Decorator - Production-Grade Implementation
"""

import time
import functools
import logging
from typing import Callable, Type, Tuple, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class RetryMetrics:
    """Track retry statistics for monitoring."""
    def __init__(self):
        self.total_calls = 0
        self.retry_needed = 0
        self.successful_after_retry = 0
        self.total_retries = 0
    
    def record_call(self):
        self.total_calls += 1
    
    def record_retry(self):
        self.retry_needed += 1
        self.total_retries += 1
    
    def record_success_after_retry(self):
        self.successful_after_retry += 1
    
    def get_stats(self) -> dict:
        return {
            "total_calls": self.total_calls,
            "retry_rate": f"{(self.retry_needed / max(self.total_calls, 1)) * 100:.2f}%",
            "success_after_retry_rate": f"{(self.successful_after_retry / max(self.retry_needed, 1)) * 100:.2f}%",
            "avg_retries": f"{self.total_retries / max(self.total_calls, 1):.2f}",
        }


# Global metrics instance
metrics = RetryMetrics()


def retry(
    attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    log_enabled: bool = True
) -> Callable:
    """
    Decorator that retries a function on failure with exponential backoff.
    
    Args:
        attempts: Maximum number of attempts (including first try)
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each failure
        exceptions: Tuple of exception types to catch and retry
        log_enabled: Whether to log retry attempts
    
    Returns:
        Decorated function with retry logic
    
    Example:
        @retry(attempts=3, delay=1, exceptions=(ConnectionError,))
        def fetch_data():
            return requests.get("https://api.example.com/data")
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            metrics.record_call()
            current_delay = delay
            last_exception = None
            needed_retry = False
            
            for attempt in range(1, attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    
                    # Track successful retry
                    if needed_retry:
                        metrics.record_success_after_retry()
                        if log_enabled:
                            logger.info(f"✅ {func.__name__} succeeded on attempt {attempt}/{attempts}")
                    
                    return result
                    
                except exceptions as e:
                    last_exception = e
                    needed_retry = True
                    
                    if attempt < attempts:
                        metrics.record_retry()
                        if log_enabled:
                            logger.warning(
                                f"⚠️  {func.__name__} attempt {attempt}/{attempts} failed: {type(e).__name__}: {e}"
                            )
                            logger.info(f"🔄 Retrying in {current_delay:.1f}s...")
                        
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        if log_enabled:
                            logger.error(
                                f"❌ {func.__name__} failed after {attempts} attempts. Giving up."
                            )
                        raise
            
            # This should never be reached, but satisfies type checker
            raise last_exception
        
        return wrapper
    return decorator


def get_retry_metrics() -> dict:
    """Get current retry metrics."""
    return metrics.get_stats()


def reset_retry_metrics():
    """Reset retry metrics (useful for testing)."""
    global metrics
    metrics = RetryMetrics()
