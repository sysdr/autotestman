"""
Page Object: ShadowSearchPage
Encapsulates all locators and actions for the Shadow DOM fixture.
"""
from dataclasses import dataclass
from playwright.async_api import Page, Locator


@dataclass
class ShadowSearchPage:
    page: Page
    url: str

    async def navigate(self) -> None:
        await self.page.goto(self.url)
        # Wait for the custom element to register and render
        await self.page.locator("custom-search").wait_for()

    # ── Shadow DOM Locators (auto-piercing via `>>`) ──────────────────────
    @property
    def search_input(self) -> Locator:
        """<custom-search> shadow root → <input>"""
        return self.page.locator("custom-search >> input[data-testid='shadow-input']")

    @property
    def search_button(self) -> Locator:
        """<custom-search> shadow root → <button>"""
        return self.page.locator("custom-search >> button[data-testid='shadow-button']")

    @property
    def result_div(self) -> Locator:
        """<custom-search> shadow root → result <div>"""
        return self.page.locator("custom-search >> [data-testid='shadow-result']")

    # ── Nested Shadow Locators ────────────────────────────────────────────
    @property
    def nested_button(self) -> Locator:
        """<nested-panel> → <inner-button> → <button> (two shadow boundaries)"""
        return self.page.locator(
            "nested-panel >> inner-button >> [data-testid='nested-button']"
        )

    @property
    def nested_message(self) -> Locator:
        """<nested-panel> → <inner-button> → result message div"""
        return self.page.locator(
            "nested-panel >> inner-button >> [data-testid='nested-msg']"
        )

    # ── Actions ───────────────────────────────────────────────────────────
    async def search(self, query: str) -> None:
        await self.search_input.fill(query)
        await self.search_button.click()

    async def get_result_text(self) -> str:
        return (await self.result_div.text_content() or "").strip()

    async def activate_nested(self) -> None:
        await self.nested_button.click()

    async def get_nested_message(self) -> str:
        return (await self.nested_message.text_content() or "").strip()
