#!/bin/bash

# UQAP Project Setup Script
# Generates all required files for the automation project

set -e  # Exit on error

PROJECT_ROOT="uqap-lesson-01"
SOURCES_DIR="$PROJECT_ROOT/src"
SCRIPTS_DIR="$PROJECT_ROOT/scripts"
CONFIG_DIR="$PROJECT_ROOT/config"
LOGS_DIR="$PROJECT_ROOT/logs"

echo "🚀 Starting UQAP Project Setup..."

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p "$SOURCES_DIR/automation"
mkdir -p "$SOURCES_DIR/api"
mkdir -p "$SOURCES_DIR/dashboard"
mkdir -p "$SCRIPTS_DIR"
mkdir -p "$CONFIG_DIR"
mkdir -p "$LOGS_DIR"
mkdir -p "$PROJECT_ROOT/tests"

echo "✓ Directory structure created"

# Generate configuration files
echo "📝 Generating configuration files..."

# API Configuration
cat > "$CONFIG_DIR/api_config.json" << 'EOF'
{
  "host": "localhost",
  "port": 8000,
  "debug": true,
  "metrics_enabled": true
}
EOF

# Dashboard Configuration
cat > "$CONFIG_DIR/dashboard_config.json" << 'EOF'
{
  "host": "localhost",
  "port": 8080,
  "refresh_interval": 5,
  "metrics_endpoint": "http://localhost:8000/metrics"
}
EOF

# Service Configuration
cat > "$CONFIG_DIR/services.json" << 'EOF'
{
  "api": {
    "script": "scripts/start_api.sh",
    "port": 8000,
    "pid_file": "logs/api.pid"
  },
  "dashboard": {
    "script": "scripts/start_dashboard.sh",
    "port": 8080,
    "pid_file": "logs/dashboard.pid"
  }
}
EOF

echo "✓ Configuration files generated"

# Generate API service
echo "📝 Generating API service..."

cat > "$SOURCES_DIR/api/__init__.py" << 'EOF'
"""UQAP API Service"""
__version__ = "0.1.0"
EOF

cat > "$SOURCES_DIR/api/server.py" << 'ENDOFFILE'
#!/usr/bin/env python3
"""
UQAP API Server
Provides metrics endpoint for dashboard
"""

import json
import time
from pathlib import Path
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Metrics storage
metrics = {
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "total_tests_run": 0,
    "tests_passed": 0,
    "tests_failed": 0,
    "uptime_seconds": 0,
    "last_update": time.time()
}

start_time = time.time()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200

@app.route('/metrics', methods=['GET'])
def get_metrics():
    """Get current metrics"""
    metrics["uptime_seconds"] = int(time.time() - start_time)
    metrics["last_update"] = time.time()
    return jsonify(metrics), 200

@app.route('/metrics/update', methods=['POST'])
def update_metrics():
    """Update metrics (called by demo script)"""
    global metrics
    data = request.get_json() or {}
    
    if "total_requests" in data:
        metrics["total_requests"] += data.get("total_requests", 0)
    if "successful_requests" in data:
        metrics["successful_requests"] += data.get("successful_requests", 0)
    if "failed_requests" in data:
        metrics["failed_requests"] += data.get("failed_requests", 0)
    if "total_tests_run" in data:
        metrics["total_tests_run"] += data.get("total_tests_run", 0)
    if "tests_passed" in data:
        metrics["tests_passed"] += data.get("tests_passed", 0)
    if "tests_failed" in data:
        metrics["tests_failed"] += data.get("tests_failed", 0)
    
    metrics["last_update"] = time.time()
    return jsonify({"status": "updated", "metrics": metrics}), 200

@app.route('/metrics/reset', methods=['POST'])
def reset_metrics():
    """Reset all metrics"""
    global metrics, start_time
    start_time = time.time()
    metrics = {
        "total_requests": 0,
        "successful_requests": 0,
        "failed_requests": 0,
        "total_tests_run": 0,
        "tests_passed": 0,
        "tests_failed": 0,
        "uptime_seconds": 0,
        "last_update": time.time()
    }
    return jsonify({"status": "reset", "metrics": metrics}), 200

if __name__ == '__main__':
    config_path = Path(__file__).parent.parent.parent / "config" / "api_config.json"
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
            host = config.get("host", "localhost")
            port = config.get("port", 8000)
            debug = config.get("debug", True)
    else:
        host = "localhost"
        port = 8000
        debug = True
    
    print(f"🚀 Starting API server on {host}:{port}")
    app.run(host=host, port=port, debug=debug)
ENDOFFILE

chmod +x "$SOURCES_DIR/api/server.py"

echo "✓ API service generated"

# Generate Dashboard
echo "📝 Generating Dashboard..."

cat > "$SOURCES_DIR/dashboard/__init__.py" << 'EOF'
"""UQAP Dashboard"""
__version__ = "0.1.0"
EOF

cat > "$SOURCES_DIR/dashboard/app.py" << 'ENDOFFILE'
#!/usr/bin/env python3
"""
UQAP Dashboard
Displays real-time metrics from API
"""

import json
import time
import requests
from pathlib import Path
from flask import Flask, render_template_string
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Dashboard HTML Template
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UQAP Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        h1 {
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .metric-card {
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
        .metric-label {
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
        }
        .metric-value.zero {
            color: #999;
        }
        .status {
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-indicator.online {
            background: #10b981;
        }
        .status-indicator.offline {
            background: #ef4444;
        }
        .last-update {
            color: #666;
            font-size: 0.9em;
            margin-top: 10px;
        }
        .error-message {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #c33;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 UQAP Metrics Dashboard</h1>
        
        <div class="status" id="status">
            <span class="status-indicator offline" id="statusIndicator"></span>
            <span id="statusText">Connecting...</span>
            <div class="last-update" id="lastUpdate"></div>
        </div>
        
        <div id="errorContainer"></div>
        
        <div class="metrics-grid" id="metricsGrid">
            <div class="metric-card">
                <div class="metric-label">Total Requests</div>
                <div class="metric-value zero" id="totalRequests">0</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Successful Requests</div>
                <div class="metric-value zero" id="successfulRequests">0</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Failed Requests</div>
                <div class="metric-value zero" id="failedRequests">0</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Total Tests Run</div>
                <div class="metric-value zero" id="totalTestsRun">0</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Tests Passed</div>
                <div class="metric-value zero" id="testsPassed">0</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Tests Failed</div>
                <div class="metric-value zero" id="testsFailed">0</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Uptime (seconds)</div>
                <div class="metric-value" id="uptime">0</div>
            </div>
        </div>
    </div>

    <script>
        const METRICS_ENDPOINT = 'http://localhost:8000/metrics';
        const REFRESH_INTERVAL = 5000; // 5 seconds

        function updateMetrics() {
            fetch(METRICS_ENDPOINT)
                .then(response => {
                    if (!response.ok) throw new Error('Network response was not ok');
                    return response.json();
                })
                .then(data => {
                    // Update status
                    document.getElementById('statusIndicator').className = 'status-indicator online';
                    document.getElementById('statusText').textContent = 'API Online';
                    
                    // Clear error
                    document.getElementById('errorContainer').innerHTML = '';
                    
                    // Update metrics
                    updateMetric('totalRequests', data.total_requests || 0);
                    updateMetric('successfulRequests', data.successful_requests || 0);
                    updateMetric('failedRequests', data.failed_requests || 0);
                    updateMetric('totalTestsRun', data.total_tests_run || 0);
                    updateMetric('testsPassed', data.tests_passed || 0);
                    updateMetric('testsFailed', data.tests_failed || 0);
                    updateMetric('uptime', data.uptime_seconds || 0);
                    
                    // Update last update time
                    const lastUpdate = new Date(data.last_update * 1000);
                    document.getElementById('lastUpdate').textContent = 
                        `Last updated: ${lastUpdate.toLocaleTimeString()}`;
                })
                .catch(error => {
                    document.getElementById('statusIndicator').className = 'status-indicator offline';
                    document.getElementById('statusText').textContent = 'API Offline';
                    document.getElementById('errorContainer').innerHTML = 
                        `<div class="error-message">Error: ${error.message}. Make sure the API server is running on port 8000.</div>`;
                });
        }

        function updateMetric(id, value) {
            const element = document.getElementById(id);
            element.textContent = value.toLocaleString();
            
            // Remove zero class if value is not zero
            if (value > 0) {
                element.classList.remove('zero');
            } else {
                element.classList.add('zero');
            }
        }

        // Initial load
        updateMetrics();
        
        // Auto-refresh
        setInterval(updateMetrics, REFRESH_INTERVAL);
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Render dashboard"""
    return render_template_string(DASHBOARD_HTML)

if __name__ == '__main__':
    config_path = Path(__file__).parent.parent.parent / "config" / "dashboard_config.json"
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
            host = config.get("host", "localhost")
            port = config.get("port", 8080)
    else:
        host = "localhost"
        port = 8080
    
    print(f"🚀 Starting Dashboard on {host}:{port}")
    app.run(host=host, port=port, debug=False)
ENDOFFILE

chmod +x "$SOURCES_DIR/dashboard/app.py"

echo "✓ Dashboard generated"

# Generate startup scripts
echo "📝 Generating startup scripts..."

# Start API script
cat > "$SCRIPTS_DIR/start_api.sh" << 'EOF'
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
python3 "$API_SCRIPT" > "$PROJECT_ROOT/logs/api.log" 2>&1 &
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
EOF

chmod +x "$SCRIPTS_DIR/start_api.sh"

# Start Dashboard script
cat > "$SCRIPTS_DIR/start_dashboard.sh" << 'EOF'
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
python3 "$DASHBOARD_SCRIPT" > "$PROJECT_ROOT/logs/dashboard.log" 2>&1 &
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
EOF

chmod +x "$SCRIPTS_DIR/start_dashboard.sh"

# Stop scripts
cat > "$SCRIPTS_DIR/stop_api.sh" << 'EOF'
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
EOF

chmod +x "$SCRIPTS_DIR/stop_api.sh"

cat > "$SCRIPTS_DIR/stop_dashboard.sh" << 'EOF'
#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PID_FILE="$PROJECT_ROOT/logs/dashboard.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        kill "$PID"
        echo "✓ Dashboard server stopped (PID: $PID)"
    else
        echo "⚠️  Process $PID not found"
    fi
    rm -f "$PID_FILE"
else
    echo "⚠️  PID file not found. Dashboard may not be running."
fi
EOF

chmod +x "$SCRIPTS_DIR/stop_dashboard.sh"

# Check services script
cat > "$SCRIPTS_DIR/check_services.sh" << 'EOF'
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
EOF

chmod +x "$SCRIPTS_DIR/check_services.sh"

echo "✓ Startup scripts generated"

# Generate demo script
echo "📝 Generating demo script..."

cat > "$SCRIPTS_DIR/run_demo.sh" << 'EOF'
#!/bin/bash

# Demo script to update dashboard metrics

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
API_URL="http://localhost:8000"

echo "🎬 Running UQAP Demo..."

# Check if API is running
if ! curl -s "$API_URL/health" > /dev/null; then
    echo "❌ Error: API server is not running. Start it with: scripts/start_api.sh"
    exit 1
fi

echo "✓ API server is accessible"

# Update metrics with demo data
echo "📊 Updating metrics..."

# Simulate test execution
curl -s -X POST "$API_URL/metrics/update" \
    -H "Content-Type: application/json" \
    -d '{
        "total_requests": 10,
        "successful_requests": 8,
        "failed_requests": 2,
        "total_tests_run": 15,
        "tests_passed": 12,
        "tests_failed": 3
    }' > /dev/null

echo "✓ Metrics updated"

# Wait a moment
sleep 1

# Get current metrics
echo ""
echo "📈 Current Metrics:"
curl -s "$API_URL/metrics" | python3 -m json.tool

echo ""
echo "✓ Demo completed! Check dashboard at http://localhost:8080"
EOF

chmod +x "$SCRIPTS_DIR/run_demo.sh"

echo "✓ Demo script generated"

# Generate test script
echo "📝 Generating test script..."

cat > "$SCRIPTS_DIR/run_tests.sh" << 'EOF'
#!/bin/bash

# Run all tests

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🧪 Running tests..."

cd "$PROJECT_ROOT"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run pytest
pytest tests/ -v --tb=short

TEST_EXIT_CODE=$?

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✓ All tests passed"
else
    echo "✗ Some tests failed"
fi

exit $TEST_EXIT_CODE
EOF

chmod +x "$SCRIPTS_DIR/run_tests.sh"

echo "✓ Test script generated"

# Generate requirements file for additional dependencies
echo "📝 Generating requirements file..."

cat > "$PROJECT_ROOT/requirements.txt" << 'EOF'
flask>=3.0.0
flask-cors>=4.0.0
requests>=2.31.0
EOF

echo "✓ Requirements file generated"

echo ""
echo "✅ Setup complete!"
echo ""
echo "Generated files:"
echo "  - Configuration files in config/"
echo "  - API service in src/api/"
echo "  - Dashboard in src/dashboard/"
echo "  - Startup scripts in scripts/"
echo "  - Demo script in scripts/"
echo ""
echo "Next steps:"
echo "  1. Install additional dependencies: pip install -r requirements.txt"
echo "  2. Start API: scripts/start_api.sh"
echo "  3. Start Dashboard: scripts/start_dashboard.sh"
echo "  4. Run demo: scripts/run_demo.sh"
echo "  5. Run tests: scripts/run_tests.sh"
