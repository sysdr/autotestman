"""
Lesson 38: Shadow DOM Handling
Test suite — all tests interact with real Shadow DOM elements.
"""
import pytest
from playwright.async_api import Page, expect
from pages.shadow_search_page import ShadowSearchPage


# ── Fixture ───────────────────────────────────────────────────────────────
@pytest.fixture()
async def shadow_page(page: Page, local_server: str) -> ShadowSearchPage:
    sp = ShadowSearchPage(page=page, url=local_server)
    await sp.navigate()
    return sp


# ── Tests ─────────────────────────────────────────────────────────────────
@pytest.mark.asyncio
async def test_fill_shadow_input(shadow_page: ShadowSearchPage) -> None:
    """Can we type into an input that lives inside a shadow root?"""
    await shadow_page.search_input.fill("playwright shadow dom")
    value = await shadow_page.search_input.input_value()
    assert value == "playwright shadow dom", (
        f"Expected 'playwright shadow dom' but got '{value}'"
    )


@pytest.mark.asyncio
async def test_shadow_button_click(shadow_page: ShadowSearchPage) -> None:
    """Does clicking the shadow button produce the correct result text?"""
    await shadow_page.search("UQAP framework")
    result = await shadow_page.get_result_text()
    assert "Results for: UQAP framework" in result, (
        f"Unexpected result text: '{result}'"
    )


@pytest.mark.asyncio
async def test_shadow_element_visibility(shadow_page: ShadowSearchPage) -> None:
    """Shadow elements should be visible and actionable without JS injection."""
    await expect(shadow_page.search_input).to_be_visible()
    await expect(shadow_page.search_button).to_be_visible()


@pytest.mark.asyncio
async def test_nested_shadow_dom(shadow_page: ShadowSearchPage) -> None:
    """Two shadow boundaries deep — still works with chained >> combinators."""
    await shadow_page.activate_nested()
    msg = await shadow_page.get_nested_message()
    assert msg == "Nested shadow activated!", (
        f"Nested shadow message incorrect: '{msg}'"
    )
