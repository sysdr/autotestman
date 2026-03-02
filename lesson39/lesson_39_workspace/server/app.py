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
