"""
Interactive Demo - See Retry Decorator in Action
"""

import sys
from pathlib import Path
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.retry_decorator import retry, get_retry_metrics, reset_retry_metrics
from demo.flaky_api_simulator import FlakinesSimulator


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_basic_retry():
    """Demonstrate basic retry functionality."""
    print_header("Demo 1: Basic Retry with Exponential Backoff")
    
    simulator = FlakinesSimulator(failure_rate=0.7)
    
    @retry(attempts=3, delay=0.5, backoff=2.0, exceptions=(ConnectionError,))
    def fetch_data():
        return simulator.flaky_network_call("user_data")
    
    print("Calling flaky API endpoint...")
    start = time.time()
    result = fetch_data()
    duration = time.time() - start
    
    print(f"\n✅ Success! Got: {result}")
    print(f"⏱️  Total time: {duration:.2f}s")


def demo_retry_metrics():
    """Demonstrate retry metrics tracking."""
    print_header("Demo 2: Retry Metrics Tracking")
    
    reset_retry_metrics()
    
    stable_sim = FlakinesSimulator(failure_rate=0)
    flaky_sim = FlakinesSimulator(failure_rate=0.8)
    
    @retry(attempts=3, delay=0.1, exceptions=(ConnectionError,))
    def stable_call():
        return stable_sim.flaky_network_call()
    
    @retry(attempts=3, delay=0.1, exceptions=(ConnectionError,))
    def flaky_call():
        return flaky_sim.flaky_network_call()
    
    # Make multiple calls
    print("Making 5 stable calls and 3 flaky calls...\n")
    for i in range(5):
        stable_call()
        stable_sim.reset()
    
    for i in range(3):
        flaky_call()
        flaky_sim.reset()
    
    metrics = get_retry_metrics()
    print("📊 Retry Metrics:")
    for key, value in metrics.items():
        print(f"   {key}: {value}")


def demo_failure_after_retries():
    """Demonstrate function failing after all retries."""
    print_header("Demo 3: Giving Up After Max Retries")
    
    simulator = FlakinesSimulator()
    
    @retry(attempts=3, delay=0.2, exceptions=(RuntimeError,))
    def always_fails():
        return simulator.always_fails()
    
    print("Calling function that always fails...")
    try:
        always_fails()
    except RuntimeError as e:
        print(f"\n❌ Function failed as expected: {e}")
        print(f"   Total attempts made: {simulator.call_count}")


def main():
    """Run all demos."""
    print("\n" + "🚀" * 30)
    print("  RETRY DECORATOR INTERACTIVE DEMO")
    print("🚀" * 30)
    
    demo_basic_retry()
    time.sleep(1)
    
    demo_retry_metrics()
    time.sleep(1)
    
    demo_failure_after_retries()
    
    print("\n" + "=" * 60)
    print("  Demo Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Run tests: pytest tests/ -v")
    print("  2. Check utils/retry_decorator.py for implementation")
    print("  3. Try modifying retry parameters (attempts, delay, backoff)")
    print()


if __name__ == "__main__":
    main()
