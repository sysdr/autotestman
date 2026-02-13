"""
app/demo_server.py
Simple HTTP server for testing login automation.
"""

from flask import Flask, send_from_directory, redirect
import os
from pathlib import Path

app = Flask(__name__)

# Get the directory where this script is located (app/)
BASE_DIR = Path(__file__).parent

@app.route('/')
def index():
    return redirect('/login.html')

@app.route('/login.html')
def login():
    return send_from_directory(BASE_DIR, 'login.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory(BASE_DIR, path)

if __name__ == '__main__':
    print("\n" + "="*50)
    print("UQAP Demo Server Starting...")
    print("Login page: http://localhost:8000/login.html")
    print("="*50 + "\n")
    app.run(host='0.0.0.0', port=8000, debug=True)