"""
tests/test_graphql_mock.py
Lesson 48: Mocking APIs
Tests: GraphQL POST payload construction + response field validation
"""
from __future__ import annotations

import requests
import pytest

from .conftest import MOCK_GRAPHQL_URL, MOCK_PRODUCT_RESPONSE


# ── GraphQL Query Definitions ─────────────────────────────────────────────────

GET_PRODUCT_QUERY = """
    query GetProduct($id: ID!) {
        product(id: $id) {
            id
            name
            price
            inStock
            tags
        }
    }
"""


def build_graphql_payload(query: str, variables: dict) -> dict:
    """Build a standard GraphQL POST payload."""
    return {"query": query, "variables": variables}


def post_graphql(url: str, query: str, variables: dict) -> requests.Response:
    """Send a GraphQL POST request and return the raw response."""
    payload = build_graphql_payload(query, variables)
    return requests.post(
        url,
        json=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        timeout=10
    )


# ── Test Cases ────────────────────────────────────────────────────────────────

class TestGraphQLMockBasic:
    """Core field validation against a mocked GraphQL response."""

    def test_status_code_is_200(self, mock_graphql_success):
        """HTTP layer: response must be 200."""
        resp = post_graphql(MOCK_GRAPHQL_URL, GET_PRODUCT_QUERY, {"id": "prod_42"})
        assert resp.status_code == 200, f"Expected 200, got {resp.status_code}"

    def test_response_has_data_key(self, mock_graphql_success):
        """GraphQL contract: top-level 'data' key must exist."""
        resp = post_graphql(MOCK_GRAPHQL_URL, GET_PRODUCT_QUERY, {"id": "prod_42"})
        body = resp.json()
        assert "data" in body, "Missing 'data' key in GraphQL response"
        assert "errors" not in body, "Unexpected 'errors' key in successful response"

    def test_product_id_field(self, mock_graphql_success):
        """Field: product.id must match requested ID."""
        resp = post_graphql(MOCK_GRAPHQL_URL, GET_PRODUCT_QUERY, {"id": "prod_42"})
        product = resp.json()["data"]["product"]
        assert product["id"] == "prod_42"

    def test_product_name_field(self, mock_graphql_success):
        """Field: product.name must be a non-empty string."""
        resp = post_graphql(MOCK_GRAPHQL_URL, GET_PRODUCT_QUERY, {"id": "prod_42"})
        product = resp.json()["data"]["product"]
        assert isinstance(product["name"], str)
        assert len(product["name"]) > 0
        assert product["name"] == "Quantum Keyboard"

    def test_product_price_is_float(self, mock_graphql_success):
        """Field: product.price must be a positive float."""
        resp = post_graphql(MOCK_GRAPHQL_URL, GET_PRODUCT_QUERY, {"id": "prod_42"})
        product = resp.json()["data"]["product"]
        assert isinstance(product["price"], float),             f"Expected float, got {type(product['price'])}"
        assert product["price"] > 0
        assert product["price"] == 149.99

    def test_product_in_stock_is_boolean(self, mock_graphql_success):
        """Field: product.inStock must be a boolean True."""
        resp = post_graphql(MOCK_GRAPHQL_URL, GET_PRODUCT_QUERY, {"id": "prod_42"})
        product = resp.json()["data"]["product"]
        assert isinstance(product["inStock"], bool),             f"Expected bool, got {type(product['inStock'])}"
        assert product["inStock"] is True

    def test_product_tags_is_list(self, mock_graphql_success):
        """Field: product.tags must be a non-empty list of strings."""
        resp = post_graphql(MOCK_GRAPHQL_URL, GET_PRODUCT_QUERY, {"id": "prod_42"})
        product = resp.json()["data"]["product"]
        assert isinstance(product["tags"], list)
        assert len(product["tags"]) > 0
        assert all(isinstance(t, str) for t in product["tags"])


class TestGraphQLMockCallVerification:
    """Verify the mock was called correctly (no double-calls, right method)."""

    def test_mock_called_exactly_once(self, mock_graphql_success):
        """API hygiene: exactly one HTTP call should be made per test."""
        post_graphql(MOCK_GRAPHQL_URL, GET_PRODUCT_QUERY, {"id": "prod_42"})
        assert len(mock_graphql_success.calls) == 1,             f"Expected 1 call, got {len(mock_graphql_success.calls)}"

    def test_request_method_is_post(self, mock_graphql_success):
        """Protocol check: GraphQL must use POST, never GET."""
        post_graphql(MOCK_GRAPHQL_URL, GET_PRODUCT_QUERY, {"id": "prod_42"})
        call = mock_graphql_success.calls[0]
        assert call.request.method == "POST"

    def test_request_contains_query_key(self, mock_graphql_success):
        """Payload check: request body must contain 'query' key."""
        import json
        post_graphql(MOCK_GRAPHQL_URL, GET_PRODUCT_QUERY, {"id": "prod_42"})
        call = mock_graphql_success.calls[0]
        body = json.loads(call.request.body)
        assert "query" in body
        assert "variables" in body
        assert body["variables"]["id"] == "prod_42"


class TestGraphQLMockErrorHandling:
    """Validate correct handling of GraphQL error responses."""

    def test_graphql_error_has_errors_key(self, mock_graphql_error):
        """Error contract: response must have 'errors' list when product not found."""
        resp = post_graphql(MOCK_GRAPHQL_URL, GET_PRODUCT_QUERY, {"id": "nonexistent"})
        body = resp.json()
        assert resp.status_code == 200  # GraphQL errors are still HTTP 200!
        assert "errors" in body
        assert body["data"] is None

    def test_graphql_error_message_content(self, mock_graphql_error):
        """Error field: first error must contain a human-readable message."""
        resp = post_graphql(MOCK_GRAPHQL_URL, GET_PRODUCT_QUERY, {"id": "nonexistent"})
        errors = resp.json()["errors"]
        assert len(errors) >= 1
        assert "message" in errors[0]
        assert isinstance(errors[0]["message"], str)

    def test_server_error_raises_on_status(self, mock_graphql_server_error):
        """Transport error: 500 should be detectable via response status."""
        resp = post_graphql(MOCK_GRAPHQL_URL, GET_PRODUCT_QUERY, {"id": "prod_42"})
        assert resp.status_code == 500
        # In production code, you'd do resp.raise_for_status()
        with pytest.raises(requests.exceptions.HTTPError):
            resp.raise_for_status()
