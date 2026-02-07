#!/usr/bin/env python3
"""
Simple HTTP server to serve the logging comparison dashboard
"""

import http.server
import socketserver
import webbrowser
import socket
import os
from pathlib import Path

def get_local_ip():
    """Get the local IP address"""
    try:
        # Connect to a remote address to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def main():
    PORT = 8000
    BASE_DIR = Path(__file__).parent
    
    # Change to the directory containing the HTML file
    os.chdir(BASE_DIR)
    
    Handler = http.server.SimpleHTTPRequestHandler
    
    # Try to find an available port
    for port in range(PORT, PORT + 10):
        try:
            # Bind to 0.0.0.0 to allow connections from Windows host in WSL2
            with socketserver.TCPServer(("0.0.0.0", port), Handler) as httpd:
                local_ip = get_local_ip()
                local_url = f"http://localhost:{port}/logging_comparison.html"
                network_url = f"http://{local_ip}:{port}/logging_comparison.html"
                
                print("="*70)
                print("📊 Dashboard Server Started")
                print("="*70)
                print(f"\n📍 Local URL (WSL):     {local_url}")
                print(f"🌐 Network URL:          {network_url}")
                print(f"\n💡 For Windows browser, try:")
                print(f"   http://localhost:{port}/logging_comparison.html")
                print(f"   or")
                print(f"   http://{local_ip}:{port}/logging_comparison.html")
                print(f"\n📁 Serving directory: {BASE_DIR}")
                print(f"\n💡 Press Ctrl+C to stop the server")
                print("="*70)
                
                # Try to open in browser (may not work in WSL2)
                try:
                    webbrowser.open(local_url)
                    print(f"\n✓ Attempted to open dashboard in browser")
                except Exception:
                    print(f"\n⚠ Could not open browser automatically")
                    print(f"   Please copy one of the URLs above to your browser")
                
                print("\n")
                httpd.serve_forever()
        except OSError as e:
            if "Address already in use" in str(e):
                continue
            else:
                raise
    
    print(f"❌ Could not find an available port (tried {PORT}-{PORT+9})")

if __name__ == "__main__":
    main()
