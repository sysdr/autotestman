#!/bin/bash

# Start Dashboard Service
# Checks for existing process and prevents duplicates

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DASHBOARD_SCRIPT="$PROJECT_ROOT/src/dashboard/app.py"
PID_FILE="$PROJECT_ROOT/logs/dashboard.pid"
CONFIG_FILE="$PROJECT_ROOT/config/dashboard_config.json"

# Check if script exists
if [ ! -f "$DASHBOARD_SCRIPT" ]; then
    echo "❌ Error: Dashboard script not found at $DASHBOARD_SCRIPT"
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
        echo "⚠️  Dashboard service already running with PID $OLD_PID"
        echo "   Use 'scripts/stop_dashboard.sh' to stop it first"
        exit 1
    else
        # Stale PID file
        rm -f "$PID_FILE"
    fi
fi

# Check if port is in use
PORT=$(python3 -c "import json; f=open('$CONFIG_FILE'); d=json.load(f); print(d.get('port', 8080))")
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "❌ Error: Port $PORT is already in use"
    exit 1
fi

# Activate virtual environment if it exists
if [ -d "$PROJECT_ROOT/.venv" ]; then
    source "$PROJECT_ROOT/.venv/bin/activate"
fi

# Start Dashboard server
echo "🚀 Starting Dashboard server..."
cd "$PROJECT_ROOT"
nohup python3 "$DASHBOARD_SCRIPT" > "$PROJECT_ROOT/logs/dashboard.log" 2>&1 &
DASHBOARD_PID=$!

# Save PID
echo $DASHBOARD_PID > "$PID_FILE"
echo "✓ Dashboard server started with PID $DASHBOARD_PID"
echo "  Logs: $PROJECT_ROOT/logs/dashboard.log"
echo "  PID file: $PID_FILE"

# Wait a moment and check if process is still running
sleep 2
if ! ps -p $DASHBOARD_PID > /dev/null 2>&1; then
    echo "❌ Error: Dashboard server failed to start. Check logs: $PROJECT_ROOT/logs/dashboard.log"
    rm -f "$PID_FILE"
    exit 1
fi

echo "✓ Dashboard server is running successfully"
echo "  Access at: http://localhost:$PORT"
