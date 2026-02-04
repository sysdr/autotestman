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
        host = "0.0.0.0"
        port = 8000
        debug = True
    
    print(f"🚀 Starting API server on {host}:{port}")
    app.run(host=host, port=port, debug=False, use_reloader=False)
