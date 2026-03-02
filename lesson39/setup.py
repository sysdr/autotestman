#!/usr/bin/env python3
"""
UQAP Bootcamp — Module 4: Modern Web Automation (Playwright)
Lesson 39: Download & Upload Handling
setup_lesson.py — Run this once to scaffold your full workspace.
"""

import sys
import textwrap
import threading
import time
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
# ANSI Color helpers
# ──────────────────────────────────────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def log(label: str, msg: str, color: str = CYAN) -> None:
    print(f"{color}{BOLD}[{label}]{RESET} {msg}")

def ok(msg: str)  -> None: print(f"  {GREEN}✅ {msg}{RESET}")
def err(msg: str) -> None: print(f"  {RED}❌ {msg}{RESET}")
def info(msg: str)-> None: print(f"  {YELLOW}➜  {msg}{RESET}")

# ──────────────────────────────────────────────────────────────────────────────
# Workspace layout
# ──────────────────────────────────────────────────────────────────────────────
ROOT = Path("lesson_39_workspace")

FILES: dict[Path, str] = {}

# ── server/app.py ─────────────────────────────────────────────────────────────
FILES[ROOT / "server" / "app.py"] = textwrap.dedent('''\
    """
    Minimal Flask server that supports:
      GET  /download  → sends a CSV file
      POST /upload    → accepts a file and returns JSON
    """
    from __future__ import annotations
    import io
    import csv
    from flask import Flask, request, jsonify, send_file
    from pathlib import Path

    app = Flask(__name__)
    UPLOAD_DIR = Path(__file__).parent / "received_uploads"
    UPLOAD_DIR.mkdir(exist_ok=True)


    @app.route("/")
    def index():
        """Simple HTML page with an upload form and a download link."""
        return """
        <!DOCTYPE html>
        <html lang="en">
        <head><meta charset="utf-8"><title>UQAP Test Server</title></head>
        <body>
          <h1>UQAP Lesson 39 — Test Server</h1>

          <h2>Download</h2>
          <a id="download-link" href="/download">Download report.csv</a>

          <h2>Upload</h2>
          <form id="upload-form" enctype="multipart/form-data" method="post" action="/upload">
            <input id="file-input" type="file" name="file" accept=".csv">
            <button id="submit-btn" type="submit">Upload</button>
          </form>
          <div id="upload-result"></div>

          <script>
            // Intercept form submit so the result shows in-page (for test assertion)
            document.getElementById("upload-form").addEventListener("submit", async (e) => {
              e.preventDefault();
              const data = new FormData(e.target);
              const res  = await fetch("/upload", {method: "POST", body: data});
              const json = await res.json();
              document.getElementById("upload-result").textContent = JSON.stringify(json);
            });
          </script>
        </body>
        </html>
        """


    @app.route("/download")
    def download_file():
        """Returns a deterministic CSV so we can verify checksum in tests."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id", "name", "score"])
        writer.writerows([
            (1, "Alice",   98),
            (2, "Bob",     87),
            (3, "Charlie", 76),
        ])
        output.seek(0)
        return send_file(
            io.BytesIO(output.getvalue().encode()),
            mimetype="text/csv",
            as_attachment=True,
            download_name="report.csv",
        )


    @app.route("/upload", methods=["POST"])
    def upload_file():
        """Accepts a multipart file upload and saves it."""
        if "file" not in request.files:
            return jsonify({"status": "error", "message": "no file field"}), 400

        f = request.files["file"]
        if f.filename == "":
            return jsonify({"status": "error", "message": "empty filename"}), 400

        dest = UPLOAD_DIR / f.filename  # type: ignore[arg-type]
        f.save(dest)
        return jsonify({
            "status":   "success",
            "filename": f.filename,
            "bytes":    dest.stat().st_size,
        })


    if __name__ == "__main__":
        app.run(port=5050, debug=False)
''')

# ── test_data/sample_upload.csv ───────────────────────────────────────────────
FILES[ROOT / "test_data" / "sample_upload.csv"] = textwrap.dedent("""\
    id,product,qty
    1,Widget A,10
    2,Widget B,25
    3,Widget C,7
""")

# ── pages/upload_download_page.py ─────────────────────────────────────────────
FILES[ROOT / "pages" / "upload_download_page.py"] = textwrap.dedent('''\
    """
    Page Object for the UQAP Lesson 39 test server.
    Wraps all Playwright interactions so tests stay declarative.
    """
    from __future__ import annotations
    from dataclasses import dataclass
    from pathlib import Path
    from playwright.sync_api import Page, Download, Response


    @dataclass
    class UploadResult:
        status:   str
        filename: str
        bytes:    int


    class UploadDownloadPage:
        URL = "http://localhost:5050"

        def __init__(self, page: Page) -> None:
            self._page = page

        # ── navigation ────────────────────────────────────────────────────────
        def navigate(self) -> None:
            self._page.goto(self.URL, wait_until="domcontentloaded")

        # ── download ──────────────────────────────────────────────────────────
        def trigger_download(self) -> Download:
            """
            Arms the download listener BEFORE clicking.
            Returns the Download object only after the file is fully written.
            This is the pattern that eliminates time.sleep().
            """
            with self._page.expect_download() as dl_info:
                self._page.locator("#download-link").click()
            return dl_info.value  # blocks until download complete

        # ── upload ────────────────────────────────────────────────────────────
        def upload_file(self, file_path: Path) -> UploadResult:
            """
            Injects file into the hidden <input type="file"> via CDP.
            Arms the response listener BEFORE clicking submit.
            Returns parsed JSON from the server response.
            """
            self._page.locator("#file-input").set_input_files(file_path)

            with self._page.expect_response(
                lambda r: "/upload" in r.url and r.status == 200
            ) as resp_info:
                self._page.locator("#submit-btn").click()

            data: dict = resp_info.value.json()
            return UploadResult(
                status=data["status"],
                filename=data["filename"],
                bytes=data["bytes"],
            )
''')

# ── utils/server_manager.py ───────────────────────────────────────────────────
FILES[ROOT / "utils" / "server_manager.py"] = textwrap.dedent('''\
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
''')

# ── conftest.py ───────────────────────────────────────────────────────────────
FILES[ROOT / "conftest.py"] = textwrap.dedent('''\
    """
    pytest fixtures shared across the lesson.
    The server fixture is session-scoped — started once, reused for all tests.
    """
    from __future__ import annotations
    import pytest
    from playwright.sync_api import Page, BrowserContext
    from utils.server_manager import start_server
    from pages.upload_download_page import UploadDownloadPage


    @pytest.fixture(scope="session", autouse=True)
    def flask_server() -> None:
        """Ensure the local test server is running for the entire test session."""
        start_server()


    @pytest.fixture()
    def upload_download_page(page: Page) -> UploadDownloadPage:
        """Navigate to the app and return the Page Object."""
        uq_page = UploadDownloadPage(page)
        uq_page.navigate()
        return uq_page
''')

# ── tests/test_upload_download.py ─────────────────────────────────────────────
FILES[ROOT / "tests" / "test_upload_download.py"] = textwrap.dedent('''\
    """
    Lesson 39 — Test Suite
    Demonstrates event-driven download and upload handling.
    No time.sleep() anywhere. Both tests complete in < 3s on any machine.
    """
    from __future__ import annotations
    import hashlib
    from pathlib import Path
    import pytest
    from pages.upload_download_page import UploadDownloadPage

    # Expected SHA-256 of the CSV the server always returns
    EXPECTED_ROWS = {("1", "Alice", "98"), ("2", "Bob", "87"), ("3", "Charlie", "76")}
    SAMPLE_UPLOAD = Path(__file__).parent.parent / "test_data" / "sample_upload.csv"


    def test_file_download_and_integrity(upload_download_page: UploadDownloadPage) -> None:
        """
        Trigger the download and verify the CSV content matches the known rows.
        We validate content — not just existence — because a 0-byte file passes
        an existence check but is useless in production.
        """
        download = upload_download_page.trigger_download()
        file_path = download.path()

        assert file_path is not None, "Download path is None — file not written"
        assert file_path.stat().st_size > 0, "Downloaded file is empty"

        # Parse and verify row content
        import csv
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            rows = {tuple(row) for row in reader}

        assert rows == EXPECTED_ROWS, f"CSV content mismatch: got {rows}"


    def test_file_upload_and_server_response(upload_download_page: UploadDownloadPage) -> None:
        """
        Upload a CSV and assert on the structured JSON response.
        We assert the HTTP contract — not the DOM text — because UI copy can change.
        """
        result = upload_download_page.upload_file(SAMPLE_UPLOAD)

        assert result.status   == "success",           f"Server returned: {result.status}"
        assert result.filename == "sample_upload.csv", f"Wrong filename: {result.filename}"
        assert result.bytes    >  0,                   f"Server reports 0 bytes saved"

        # Verify file size matches what we sent
        expected_bytes = SAMPLE_UPLOAD.stat().st_size
        assert result.bytes == expected_bytes, (
            f"Size mismatch: sent {expected_bytes}B, server saved {result.bytes}B"
        )
''')

# ── pytest.ini ────────────────────────────────────────────────────────────────
FILES[ROOT / "pytest.ini"] = textwrap.dedent("""\
    [pytest]
    testpaths = tests
    addopts   = -v --tb=short
""")

# ── requirements.txt ──────────────────────────────────────────────────────────
FILES[ROOT / "requirements.txt"] = textwrap.dedent("""\
    flask>=3.0
    playwright>=1.44
    pytest>=8.0
    pytest-playwright>=0.5
""")


# ──────────────────────────────────────────────────────────────────────────────
# Scaffold + Verify
# ──────────────────────────────────────────────────────────────────────────────

def scaffold_workspace() -> None:
    log("SCAFFOLD", f"Building workspace at  ./{ROOT}", CYAN)
    for path, content in FILES.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        info(f"Created  {path.relative_to(ROOT.parent)}")
    ok("All files written.")


def verify_result() -> None:
    log("VERIFY", "Checking workspace integrity …", YELLOW)
    all_ok = True
    for path in FILES:
        if path.exists() and path.stat().st_size > 0:
            ok(f"{path.relative_to(ROOT.parent)}")
        else:
            err(f"MISSING or EMPTY: {path}")
            all_ok = False

    print()
    if all_ok:
        print(f"{GREEN}{BOLD}{'─'*60}{RESET}")
        print(f"{GREEN}{BOLD}  ✅  WORKSPACE VERIFIED — all files present and non-empty{RESET}")
        print(f"{GREEN}{BOLD}{'─'*60}{RESET}")
    else:
        print(f"{RED}{BOLD}  ❌  Some files are missing. Re-run setup_lesson.py{RESET}")
        sys.exit(1)

    print()
    log("NEXT STEPS", "Run the following commands:", CYAN)
    print(f"""
  {YELLOW}cd {ROOT}{RESET}
  {YELLOW}pip install -r requirements.txt{RESET}
  {YELLOW}playwright install chromium{RESET}
  {YELLOW}pytest tests/ -v{RESET}                   # headless
  {YELLOW}pytest tests/ -v --headed{RESET}          # watch the browser
  {YELLOW}pytest tests/ -v --durations=5{RESET}     # verify no slow tests
""")


if __name__ == "__main__":
    scaffold_workspace()
    verify_result()
