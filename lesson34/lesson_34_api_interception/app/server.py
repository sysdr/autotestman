#!/usr/bin/env python3
"""Simple HTTP server for the dashboard application."""

import http.server
import json
import socketserver
from datetime import datetime
from typing import Any

PORT = 8080

class DashboardRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler for API endpoints."""
    
    def do_GET(self) -> None:
        """Handle GET requests."""
        if self.path == '/api/users/me':
            self._handle_api_request()
        else:
            # Serve static files
            super().do_GET()
    
    def _handle_api_request(self) -> None:
        """Return user data as JSON."""
        user_data = {
            "id": "usr_123456",
            "name": "Sarah Chen",
            "email": "sarah.chen@example.com",
            "role": "Senior Engineer",
            "memberSince": "2022-03-15T00:00:00Z"
        }
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(user_data).encode())
    
    def log_message(self, format: str, *args: Any) -> None:
        """Custom log format."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {format % args}")


if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), DashboardRequestHandler) as httpd:
        print(f"\n{'='*60}")
        print(f"🌐 Dashboard Server Running")
        print(f"{'='*60}")
        print(f"URL: http://localhost:{PORT}/app/index.html")
        print(f"API: http://localhost:{PORT}/api/users/me")
        print(f"{'='*60}\n")
        print("Press Ctrl+C to stop\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✓ Server stopped")
