#!/bin/bash

# Start API Service
# Checks for existing process and prevents duplicates

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
API_SCRIPT="$PROJECT_ROOT/src/api/server.py"
PID_FILE="$PROJECT_ROOT/logs/api.pid"
CONFIG_FILE="$PROJECT_ROOT/config/api_config.json"

# Check if script exists
if [ ! -f "$API_SCRIPT" ]; then
    echo "❌ Error: API script not found at $API_SCRIPT"
    exit 1
fi

# Check if config exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Error: Config file not found at $CONFIG_FILE"
    exit 1
fi

# Check for existing process
if [ -f "$PID_FILE" ]; then
    OLD_PID=$(cat "$PID_FILE")
    if ps -p "$OLD_PID" > /dev/null 2>&1; then
        echo "⚠️  API service already running with PID $OLD_PID"
        echo "   Use 'scripts/stop_api.sh' to stop it first"
        exit 1
    else
        # Stale PID file
        rm -f "$PID_FILE"
    fi
fi

# Check if port is in use
PORT=$(python3 -c "import json; f=open('$CONFIG_FILE'); d=json.load(f); print(d.get('port', 8000))")
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "❌ Error: Port $PORT is already in use"
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "$PROJECT_ROOT/.venv" ]; then
    source "$PROJECT_ROOT/.venv/bin/activate"
fi

# Start API server
echo "🚀 Starting API server..."
cd "$PROJECT_ROOT"
nohup python3 "$API_SCRIPT" > "$PROJECT_ROOT/logs/api.log" 2>&1 &
API_PID=$!

# Save PID
echo $API_PID > "$PID_FILE"
echo "✓ API server started with PID $API_PID"
echo "  Logs: $PROJECT_ROOT/logs/api.log"
echo "  PID file: $PID_FILE"

# Wait a moment and check if process is still running
sleep 2
if ! ps -p $API_PID > /dev/null 2>&1; then
    echo "❌ Error: API server failed to start. Check logs: $PROJECT_ROOT/logs/api.log"
    rm -f "$PID_FILE"
    exit 1
fi

echo "✓ API server is running successfully"
