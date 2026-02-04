#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PID_FILE="$PROJECT_ROOT/logs/api.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        kill "$PID"
        echo "✓ API server stopped (PID: $PID)"
    else
        echo "⚠️  Process $PID not found"
    fi
    rm -f "$PID_FILE"
else
    echo "⚠️  PID file not found. API may not be running."
fi
