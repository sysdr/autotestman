"""
api_client.py — Typed HTTP client for the UQAP API layer.
Lesson 44: Chaining Requests
"""
import httpx
from dataclasses import dataclass


@dataclass
class UserResponse:
    id: int
    name: str
    email: str


class ApiClient:
    """Thin wrapper around httpx.Client providing typed API methods."""

    def __init__(self, base_url: str) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=10.0)

    # ── CRUD ─────────────────────────────────────────────────────────────────

    def create_user(self, name: str, email: str) -> UserResponse:
        """POST /users — returns typed UserResponse with server-assigned ID."""
        response = self._client.post("/users", json={"name": name, "email": email})
        response.raise_for_status()
        data = response.json()
        return UserResponse(id=data["id"], name=data["name"], email=data["email"])

    def get_user(self, user_id: int) -> UserResponse:
        """GET /users/{id} — retrieves user by ID extracted from a prior response."""
        response = self._client.get(f"/users/{user_id}")
        response.raise_for_status()
        data = response.json()
        return UserResponse(id=data["id"], name=data["name"], email=data["email"])

    def delete_user(self, user_id: int) -> None:
        """DELETE /users/{id} — fixture teardown cleanup."""
        self._client.delete(f"/users/{user_id}")

    def close(self) -> None:
        self._client.close()
