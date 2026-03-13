"""
test_user_chain.py — Lesson 44: Chaining Requests
Core test: extract user_id from create_user response, use in get_user_details.
"""
import pytest
from utils.api_client import ApiClient, UserResponse


class TestRequestChaining:

    def test_get_user_matches_created_user(
        self,
        api_client: ApiClient,
        created_user: UserResponse,
    ) -> None:
        """
        Chain: create_user → extract id → get_user_details → assert consistency.
        The user_id is NEVER hardcoded; it flows through the fixture chain.
        """
        fetched = api_client.get_user(created_user.id)

        assert fetched.id == created_user.id,    "ID mismatch after retrieval"
        assert fetched.name == created_user.name, "Name mismatch — data integrity failure"
        assert fetched.email == created_user.email, "Email mismatch"

    def test_nonexistent_user_returns_404(self, api_client: ApiClient) -> None:
        """Verify server returns 404 for IDs not in the system."""
        import httpx
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            api_client.get_user(999_999)
        assert exc_info.value.response.status_code == 404

    def test_deleted_user_is_not_retrievable(
        self,
        api_client: ApiClient,
        created_user: UserResponse,
    ) -> None:
        """
        Extend the chain: create → get (ok) → delete → get (404).
        Verifies fixture teardown behaviour matches explicit delete.
        """
        import httpx

        # Confirm exists
        fetched = api_client.get_user(created_user.id)
        assert fetched.id == created_user.id

        # Delete manually (fixture teardown would also do this — double-delete is safe)
        api_client.delete_user(created_user.id)

        # Should now 404
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            api_client.get_user(created_user.id)
        assert exc_info.value.response.status_code == 404
