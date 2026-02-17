"""
Pytest fixtures for DDT tests.
Starts a local HTTP server to serve the mock login page (avoids SSL / non-existent demo URL).
"""

import socket
import threading
import time
import pytest
import functools
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path


def _find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


@pytest.fixture(scope="session")
def login_base_url():
    """Start a local HTTP server serving the mock login page; yield its base URL."""
    fixtures_dir = Path(__file__).resolve().parent / "fixtures"
    port = _find_free_port()
    handler = functools.partial(SimpleHTTPRequestHandler, directory=str(fixtures_dir))
    server = HTTPServer(("127.0.0.1", port), handler)

    def run():
        with server:
            server.serve_forever()

    thread = threading.Thread(target=run, daemon=True)
    thread.start()

    base = f"http://127.0.0.1:{port}"
    time.sleep(0.2)
    yield base
    server.shutdown()

