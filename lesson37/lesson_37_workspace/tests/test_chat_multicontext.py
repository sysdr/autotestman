"""
Lesson 37 — Multi-Context Tests
================================
Three test cases demonstrating isolated BrowserContext usage in Playwright.

Key assertions use expect().to_contain_text() — NEVER time.sleep().
"""

from playwright.sync_api import Page, BrowserContext, expect


# ── Helper ──────────────────────────────────────────────────────────────
def open_chat_page(context: BrowserContext, url: str, username: str) -> Page:
    """Open the chat app in a new page, passing the username as a query param."""
    page = context.new_page()
    page.goto(f"{url}/chat.html?user={username}")
    # Wait until the username is displayed — confirms JS executed correctly
    expect(page.locator("#username-display")).to_have_text(username)
    return page


# ── Test 1: One-Way Message ─────────────────────────────────────────────
def test_alice_sends_bob_receives(chat_contexts, chat_server_url: str):
    """
    Alice sends a message. Bob's context receives it via BroadcastChannel.
    Proves context isolation: Alice's sessionStorage != Bob's sessionStorage.
    """
    ctx_a, ctx_b = chat_contexts
    url = chat_server_url

    alice = open_chat_page(ctx_a, url, "Alice")
    bob   = open_chat_page(ctx_b, url, "Bob")

    # ── Alice types and sends ──────────────────────────────────────────
    alice.fill("#message-input", "Hey Bob! Can you hear me?")
    alice.click("#send-btn")

    # ── Bob's DOM should update — no sleep, Playwright polls internally ──
    expect(bob.locator("#chat-log")).to_contain_text("Hey Bob! Can you hear me?")

    # ── Verify Alice's message does NOT appear as "other" in her own log ─
    self_messages = alice.locator(".message.self")
    expect(self_messages.first).to_contain_text("Hey Bob! Can you hear me?")

    # ── Verify Bob received it as "other" ─────────────────────────────
    other_on_bob = bob.locator(".message.other")
    expect(other_on_bob.first).to_contain_text("Hey Bob! Can you hear me?")


# ── Test 2: Two-Way Conversation ────────────────────────────────────────
def test_bob_replies_to_alice(chat_contexts, chat_server_url: str):
    """
    Full conversation: A → B, then B → A.
    """
    ctx_a, ctx_b = chat_contexts
    url = chat_server_url

    alice = open_chat_page(ctx_a, url, "Alice")
    bob   = open_chat_page(ctx_b, url, "Bob")

    # Alice speaks first
    alice.fill("#message-input", "Hello from Alice!")
    alice.click("#send-btn")
    expect(bob.locator("#chat-log")).to_contain_text("Hello from Alice!")

    # Bob replies
    bob.fill("#message-input", "Hello from Bob!")
    bob.click("#send-btn")
    expect(alice.locator("#chat-log")).to_contain_text("Hello from Bob!")

    # Verify both messages exist in Bob's log (one self, one other)
    bob_messages = bob.locator(".message")
    expect(bob_messages).to_have_count(2)


# ── Test 3: Simultaneous Messages ───────────────────────────────────────
def test_simultaneous_messaging(chat_contexts, chat_server_url: str):
    """
    Both contexts send messages nearly simultaneously.
    Proves neither blocks the other — async event loop is not single-threaded
    at the OS level when using BroadcastChannel.
    """
    ctx_a, ctx_b = chat_contexts
    url = chat_server_url

    alice = open_chat_page(ctx_a, url, "Alice")
    bob   = open_chat_page(ctx_b, url, "Bob")

    # Pre-fill both inputs
    alice.fill("#message-input", "Alice: simultaneous ping")
    bob.fill("#message-input", "Bob: simultaneous pong")

    # Click both send buttons back-to-back (no sleep between them)
    alice.click("#send-btn")
    bob.click("#send-btn")

    # Both messages must eventually appear in both logs
    expect(alice.locator("#chat-log")).to_contain_text("Bob: simultaneous pong")
    expect(bob.locator("#chat-log")).to_contain_text("Alice: simultaneous ping")
