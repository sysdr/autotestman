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
