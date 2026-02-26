import pytest
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
import asyncio, threading, http.server, functools
from pathlib import Path

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "shadow_component.html"

# ── Tiny local file server ──────────────────────────────────────────────────
class _Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_): pass  # suppress server noise

def _start_server(directory: Path, port: int) -> None:
    handler = functools.partial(_Handler, directory=str(directory))
    srv = http.server.HTTPServer(("127.0.0.1", port), handler)
    srv.serve_forever()

@pytest.fixture(scope="session")
def local_server() -> str:
    port = 9341
    t = threading.Thread(
        target=_start_server,
        args=(FIXTURE_PATH.parent, port),
        daemon=True,
    )
    t.start()
    return f"http://127.0.0.1:{port}/{FIXTURE_PATH.name}"


# ── Playwright fixtures ─────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def browser():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(headless=True)
        yield b
        await b.close()

@pytest.fixture()
async def page(browser: Browser) -> Page:
    ctx: BrowserContext = await browser.new_context()
    p: Page = await ctx.new_page()
    yield p
    await ctx.close()
