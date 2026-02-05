#!/usr/bin/env python3
"""
Live Dashboard Server for Lesson 3
Shows real-time metrics from JSON parsing demo
"""
import json
import time
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from utils.parser import parse_users_from_file, filter_adults, filter_active_adults

class DashboardHandler(BaseHTTPRequestHandler):
    """HTTP handler for dashboard requests."""
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.get_dashboard_html().encode())
        elif self.path == '/metrics':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            metrics = self.get_metrics()
            self.wfile.write(json.dumps(metrics).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def get_metrics(self):
        """Get current metrics from data files."""
        data_file = Path(__file__).parent / "data" / "users.json"
        output_file = Path(__file__).parent / "output" / "metrics.json"
        
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "total_users": 0,
            "adults": 0,
            "active_adults": 0,
            "minors": 0,
            "parse_success_rate": 0.0,
            "test_runs": 0,
            "last_update": None
        }
        
        try:
            # Parse users from file
            users = parse_users_from_file(data_file)
            adults = filter_adults(users)
            active_adults = filter_active_adults(users)
            minors = [u for u in users if u.age is not None and u.age <= 18]
            
            # Calculate parse success rate (assuming 12 total records in original data)
            total_records = 12
            success_rate = (len(users) / total_records * 100) if total_records > 0 else 0
            
            metrics.update({
                "total_users": len(users),
                "adults": len(adults),
                "active_adults": len(active_adults),
                "minors": len(minors),
                "parse_success_rate": round(success_rate, 2)
            })
            
            # Read test run count from metrics file if it exists
            if output_file.exists():
                try:
                    with output_file.open('r') as f:
                        saved_metrics = json.load(f)
                        metrics["test_runs"] = saved_metrics.get("test_runs", 0)
                        metrics["last_update"] = saved_metrics.get("last_update")
                except:
                    pass
            
        except Exception as e:
            print(f"Error getting metrics: {e}")
        
        return metrics
    
    def get_dashboard_html(self):
        """Generate dashboard HTML with auto-refresh."""
        return '''<!DOCTYPE html>
<html>
<head>
    <title>Lesson 3 - Live Dashboard</title>
    <meta http-equiv="refresh" content="3">
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
            max-width: 1400px;
            margin: 0 auto;
        }
        .header {
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .header h1 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        .header .subtitle {
            color: #7f8c8d;
            font-size: 14px;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .metric-card {
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }
        .metric-card:hover {
            transform: translateY(-5px);
        }
        .metric-label {
            color: #7f8c8d;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }
        .metric-value {
            font-size: 48px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }
        .metric-value.zero {
            color: #e74c3c;
        }
        .metric-value.non-zero {
            color: #27ae60;
        }
        .metric-unit {
            font-size: 16px;
            color: #95a5a6;
            margin-left: 5px;
        }
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-indicator.live {
            background: #27ae60;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .footer {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: #7f8c8d;
            font-size: 12px;
        }
        .alert {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
        .alert.warning {
            background: #f8d7da;
            border-left-color: #dc3545;
        }
    </style>
    <script>
        async function loadMetrics() {
            try {
                const response = await fetch('/metrics');
                const data = await response.json();
                
                // Update metric values
                document.getElementById('total-users').textContent = data.total_users || 0;
                document.getElementById('adults').textContent = data.adults || 0;
                document.getElementById('active-adults').textContent = data.active_adults || 0;
                document.getElementById('minors').textContent = data.minors || 0;
                document.getElementById('success-rate').textContent = (data.parse_success_rate || 0).toFixed(1);
                document.getElementById('test-runs').textContent = data.test_runs || 0;
                document.getElementById('last-update').textContent = data.last_update || 'Never';
                
                // Check for zero values and add warnings
                const zeroMetrics = [];
                if (data.total_users === 0) zeroMetrics.push('Total Users');
                if (data.adults === 0) zeroMetrics.push('Adults');
                if (data.active_adults === 0) zeroMetrics.push('Active Adults');
                
                const alertDiv = document.getElementById('alerts');
                if (zeroMetrics.length > 0) {
                    alertDiv.innerHTML = '<div class="alert warning">[WARNING] Warning: The following metrics are zero: ' + zeroMetrics.join(', ') + '. Run the demo to update them.</div>';
                } else {
                    alertDiv.innerHTML = '<div class="alert">[OK] All metrics are updating correctly!</div>';
                }
                
                // Update value classes
                document.getElementById('total-users').className = 'metric-value ' + (data.total_users > 0 ? 'non-zero' : 'zero');
                document.getElementById('adults').className = 'metric-value ' + (data.adults > 0 ? 'non-zero' : 'zero');
                document.getElementById('active-adults').className = 'metric-value ' + (data.active_adults > 0 ? 'non-zero' : 'zero');
                
            } catch (error) {
                console.error('Error loading metrics:', error);
            }
        }
        
        // Load metrics on page load and every 2 seconds
        window.addEventListener('load', () => {
            loadMetrics();
            setInterval(loadMetrics, 2000);
        });
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><span class="status-indicator live"></span>Lesson 3 - Live Metrics Dashboard</h1>
            <div class="subtitle">Real-time JSON Parsing Metrics | Auto-refreshing every 2 seconds</div>
        </div>
        
        <div id="alerts"></div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">Total Users Parsed</div>
                <div class="metric-value" id="total-users">0</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Adults (age > 18)</div>
                <div class="metric-value" id="adults">0</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Active Adults</div>
                <div class="metric-value" id="active-adults">0</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Minors (age &lt;= 18)</div>
                <div class="metric-value" id="minors">0</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Parse Success Rate</div>
                <div class="metric-value" id="success-rate">0.0<span class="metric-unit">%</span></div>
            </div>
            
            <div class="metric-card">
                <div class="metric-label">Test Runs</div>
                <div class="metric-value" id="test-runs">0</div>
            </div>
        </div>
        
        <div class="footer">
            Last Update: <span id="last-update">Loading...</span> | 
            Dashboard running on port 8080
        </div>
    </div>
</body>
</html>'''

def run_server(port=8080):
    """Run the dashboard server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, DashboardHandler)
    print(f"Dashboard server starting on http://localhost:{port}")
    print("Press Ctrl+C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down dashboard server...")
        httpd.shutdown()

if __name__ == '__main__':
    run_server()
