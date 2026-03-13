"""conftest.py — Shared pytest fixtures for Lesson 48."""
import pytest
import responses as rsps_lib


MOCK_GRAPHQL_URL = "https://api.example.com/graphql"

MOCK_PRODUCT_RESPONSE = {
    "data": {
        "product": {
            "id": "prod_42",
            "name": "Quantum Keyboard",
            "price": 149.99,
            "inStock": True,
            "tags": ["mechanical", "wireless", "rgb"]
        }
    }
}

MOCK_ERROR_RESPONSE = {
    "data": None,
    "errors": [
        {"message": "Product not found", "extensions": {"code": "NOT_FOUND"}}
    ]
}


@pytest.fixture
def mock_graphql_success():
    """Fixture: mocks a successful GraphQL product query."""
    with rsps_lib.RequestsMock() as rsps:
        rsps.add(
            method=rsps_lib.POST,
            url=MOCK_GRAPHQL_URL,
            json=MOCK_PRODUCT_RESPONSE,
            status=200,
            content_type="application/json"
        )
        yield rsps
    # Mock automatically deregistered here


@pytest.fixture
def mock_graphql_error():
    """Fixture: mocks a GraphQL error response (e.g., not found)."""
    with rsps_lib.RequestsMock() as rsps:
        rsps.add(
            method=rsps_lib.POST,
            url=MOCK_GRAPHQL_URL,
            json=MOCK_ERROR_RESPONSE,
            status=200,  # GraphQL errors still return HTTP 200
            content_type="application/json"
        )
        yield rsps


@pytest.fixture
def mock_graphql_server_error():
    """Fixture: mocks a 500 Internal Server Error."""
    with rsps_lib.RequestsMock() as rsps:
        rsps.add(
            method=rsps_lib.POST,
            url=MOCK_GRAPHQL_URL,
            json={"message": "Internal Server Error"},
            status=500
        )
        yield rsps
