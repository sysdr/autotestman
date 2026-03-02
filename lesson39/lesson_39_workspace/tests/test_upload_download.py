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
