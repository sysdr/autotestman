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
            <button onclick="updateMetrics()" style="margin-top: 10px; padding: 8px 16px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 14px;">🔄 Refresh Metrics</button>
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
        const REFRESH_INTERVAL = 2000; // 2 seconds (faster refresh)

        function updateMetrics() {
            // Add cache-busting parameter to prevent caching
            const url = METRICS_ENDPOINT + '?t=' + Date.now();
            
            fetch(url, {
                method: 'GET',
                headers: {
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache'
                },
                cache: 'no-store'
            })
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
                    
                    // Update metrics - ensure we use the actual values from API
                    updateMetric('totalRequests', parseInt(data.total_requests) || 0);
                    updateMetric('successfulRequests', parseInt(data.successful_requests) || 0);
                    updateMetric('failedRequests', parseInt(data.failed_requests) || 0);
                    updateMetric('totalTestsRun', parseInt(data.total_tests_run) || 0);
                    updateMetric('testsPassed', parseInt(data.tests_passed) || 0);
                    updateMetric('testsFailed', parseInt(data.tests_failed) || 0);
                    updateMetric('uptime', parseInt(data.uptime_seconds) || 0);
                    
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
                    console.error('Metrics fetch error:', error);
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

        // Initial load immediately
        updateMetrics();
        
        // Force immediate refresh after a short delay
        setTimeout(updateMetrics, 500);
        
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
        host = "0.0.0.0"
        port = 8080
    
    print(f"🚀 Starting Dashboard on {host}:{port}")
    app.run(host=host, port=port, debug=False, use_reloader=False)
