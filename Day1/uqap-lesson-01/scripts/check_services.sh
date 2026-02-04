#!/bin/bash

# Check for duplicate services

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🔍 Checking for running services..."

# Check API
API_PID_FILE="$PROJECT_ROOT/logs/api.pid"
if [ -f "$API_PID_FILE" ]; then
    API_PID=$(cat "$API_PID_FILE")
    if ps -p "$API_PID" > /dev/null 2>&1; then
        echo "✓ API service running (PID: $API_PID)"
        
        # Check for duplicates
        API_COUNT=$(ps aux | grep -E "python.*server\.py" | grep -v grep | wc -l)
        if [ "$API_COUNT" -gt 1 ]; then
            echo "⚠️  WARNING: Multiple API processes detected!"
            ps aux | grep -E "python.*server\.py" | grep -v grep
        fi
    else
        echo "✗ API service not running (stale PID file)"
        rm -f "$API_PID_FILE"
    fi
else
    echo "✗ API service not running"
fi

# Check Dashboard
DASHBOARD_PID_FILE="$PROJECT_ROOT/logs/dashboard.pid"
if [ -f "$DASHBOARD_PID_FILE" ]; then
    DASHBOARD_PID=$(cat "$DASHBOARD_PID_FILE")
    if ps -p "$DASHBOARD_PID" > /dev/null 2>&1; then
        echo "✓ Dashboard service running (PID: $DASHBOARD_PID)"
        
        # Check for duplicates
        DASHBOARD_COUNT=$(ps aux | grep -E "python.*app\.py" | grep -v grep | wc -l)
        if [ "$DASHBOARD_COUNT" -gt 1 ]; then
            echo "⚠️  WARNING: Multiple Dashboard processes detected!"
            ps aux | grep -E "python.*app\.py" | grep -v grep
        fi
    else
        echo "✗ Dashboard service not running (stale PID file)"
        rm -f "$DASHBOARD_PID_FILE"
    fi
else
    echo "✗ Dashboard service not running"
fi
