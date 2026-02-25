import pytest
from playwright.sync_api import Playwright


@pytest.fixture(scope="function")
def chat_contexts(playwright: Playwright, chat_server_url: str):
    """
    Yield (context_a, context_b) — two page containers that share the same
    browser context so BroadcastChannel can deliver messages between Alice
    and Bob's pages. Each page still has its own sessionStorage (per-tab).
    """
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()

    # Same context twice: both pages share BroadcastChannel (same origin).
    yield context, context

    context.close()
    browser.close()


@pytest.fixture(scope="session")
def chat_server_url(tmp_path_factory):
    """
    Spin up a local HTTP server serving the chat HTML for the test session.
    Returns the base URL string.
    """
    import threading
    import http.server
    import functools
    from pathlib import Path

    html_file = Path(__file__).parent.parent / "app" / "chat.html"
    serve_dir  = html_file.parent

    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler,
        directory=str(serve_dir),
    )
    # Port 0 → OS picks a free port (avoids CI collisions)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port   = server.server_address[1]

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    url = f"http://127.0.0.1:{port}"
    yield url

    server.shutdown()
