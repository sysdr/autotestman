#!/usr/bin/env python3
"""
Demo Runner for Lesson 3
Continuously runs tests and updates metrics to demonstrate the system
"""
import json
import time
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.parser import parse_users_from_file, filter_adults, filter_active_adults

def update_metrics():
    """Run tests and update metrics file."""
    data_file = Path(__file__).parent / "data" / "users.json"
    output_file = Path(__file__).parent / "output" / "metrics.json"
    
    try:
        # Parse users
        users = parse_users_from_file(data_file)
        adults = filter_adults(users)
        active_adults = filter_active_adults(users)
        minors = [u for u in users if u.age is not None and u.age <= 18]
        
        # Calculate metrics
        total_records = 12  # Original data has 12 records
        success_rate = (len(users) / total_records * 100) if total_records > 0 else 0
        
        # Read existing metrics or create new
        if output_file.exists():
            try:
                with output_file.open('r') as f:
                    metrics = json.load(f)
            except:
                metrics = {"test_runs": 0}
        else:
            metrics = {"test_runs": 0}
        
        # Update metrics
        metrics.update({
            "timestamp": datetime.now().isoformat(),
            "total_users": len(users),
            "adults": len(adults),
            "active_adults": len(active_adults),
            "minors": len(minors),
            "parse_success_rate": round(success_rate, 2),
            "test_runs": metrics.get("test_runs", 0) + 1,
            "last_update": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        # Write metrics
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with output_file.open('w') as f:
            json.dump(metrics, f, indent=2)
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Metrics updated: "
              f"Users={len(users)}, Adults={len(adults)}, Active Adults={len(active_adults)}, "
              f"Test Runs={metrics['test_runs']}")
        
        return True
        
    except Exception as e:
        print(f"Error updating metrics: {e}")
        return False

def run_demo(interval=5):
    """Run demo continuously, updating metrics every interval seconds."""
    print("=" * 60)
    print("Lesson 3 Demo Runner")
    print("=" * 60)
    print(f"Updating metrics every {interval} seconds...")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    # Initial update
    update_metrics()
    
    try:
        while True:
            time.sleep(interval)
            update_metrics()
    except KeyboardInterrupt:
        print("\nDemo runner stopped.")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Run Lesson 3 demo')
    parser.add_argument('--interval', type=int, default=5, help='Update interval in seconds (default: 5)')
    args = parser.parse_args()
    
    run_demo(args.interval)
