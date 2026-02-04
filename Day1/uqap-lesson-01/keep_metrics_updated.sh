#!/bin/bash
# Keep metrics updated by running demo periodically

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🔄 Starting metrics updater..."
echo "This will update metrics every 10 seconds"
echo "Press Ctrl+C to stop"
echo ""

cd "$PROJECT_ROOT"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

while true; do
    echo "$(date '+%H:%M:%S') - Updating metrics..."
    python3 update_metrics.py > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "  ✓ Metrics updated"
    else
        echo "  ✗ Failed to update metrics"
    fi
    sleep 10
done
