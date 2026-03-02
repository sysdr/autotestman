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
