"""
Spins the Flask dev server in a daemon thread so pytest controls its lifecycle.
No Docker required for local dev — the server dies when the process exits.
"""
from __future__ import annotations
import sys
import time
import threading
import urllib.request
import urllib.error
from pathlib import Path


def _boot_server() -> None:
    import subprocess
    server_script = Path(__file__).parent.parent / "server" / "app.py"
    subprocess.run(
        [sys.executable, str(server_script)],
        check=False,
    )


def start_server(port: int = 5050, timeout: float = 10.0) -> None:
    """Start Flask in background thread and block until it is ready."""
    t = threading.Thread(target=_boot_server, daemon=True)
    t.start()

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            urllib.request.urlopen(f"http://localhost:{port}/", timeout=1)
            return  # server is up
        except (urllib.error.URLError, OSError):
            time.sleep(0.2)
    raise RuntimeError(f"Flask server did not start within {timeout}s")
