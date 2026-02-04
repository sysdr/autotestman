#!/bin/bash
# Quick check of current metrics

cd "$(dirname "$0")"

if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

echo "📊 Current Metrics on Server:"
echo "=============================="
python3 << 'PYTHON'
import requests
import json

try:
    r = requests.get("http://127.0.0.1:8000/metrics", timeout=5)
    r.raise_for_status()
    m = r.json()
    
    print(f"Total Requests: {m['total_requests']}")
    print(f"Successful Requests: {m['successful_requests']}")
    print(f"Failed Requests: {m['failed_requests']}")
    print(f"Total Tests Run: {m['total_tests_run']}")
    print(f"Tests Passed: {m['tests_passed']}")
    print(f"Tests Failed: {m['tests_failed']}")
    print(f"Uptime: {m['uptime_seconds']} seconds")
    
    # Check if metrics are non-zero
    if m['total_requests'] > 0 and m['total_tests_run'] > 0:
        print("\n✓ Metrics are updated (non-zero values)")
    else:
        print("\n✗ Metrics are still zero - run: python3 update_metrics.py")
        
except Exception as e:
    print(f"Error: {e}")
PYTHON
