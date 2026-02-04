#!/bin/bash

# Demo script to update dashboard metrics

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
API_URL="http://localhost:8000"

echo "🎬 Running UQAP Demo..."

# Check if API is running using Python
if ! python3 -c "import requests; requests.get('$API_URL/health', timeout=2)" 2>/dev/null; then
    echo "❌ Error: API server is not running. Start it with: scripts/start_api.sh"
    exit 1
fi

echo "✓ API server is accessible"

# Update metrics with demo data
echo "📊 Updating metrics..."

# Simulate test execution using Python
python3 << PYTHON_SCRIPT
import requests
import json

api_url = "$API_URL"

try:
    response = requests.post(
        f"{api_url}/metrics/update",
        json={
            "total_requests": 10,
            "successful_requests": 8,
            "failed_requests": 2,
            "total_tests_run": 15,
            "tests_passed": 12,
            "tests_failed": 3
        },
        timeout=5
    )
    response.raise_for_status()
    print("✓ Metrics updated")
except Exception as e:
    print(f"❌ Error updating metrics: {e}")
    exit(1)
PYTHON_SCRIPT

# Wait a moment
sleep 1

# Get current metrics
echo ""
echo "📈 Current Metrics:"
python3 << PYTHON_SCRIPT
import requests
import json

api_url = "$API_URL"

try:
    response = requests.get(f"{api_url}/metrics", timeout=5)
    response.raise_for_status()
    metrics = response.json()
    print(json.dumps(metrics, indent=2))
except Exception as e:
    print(f"❌ Error getting metrics: {e}")
    exit(1)
PYTHON_SCRIPT

echo ""
echo "✓ Demo completed! Check dashboard at http://localhost:8080"
