"""Network interception utilities for testing."""

import json
from contextlib import contextmanager
from typing import Any, Callable, Iterator

from playwright.sync_api import Page, Route


class NetworkInterceptor:
    """Utilities for intercepting and mocking network requests."""

    @staticmethod
    @contextmanager
    def mock_api_response(
        page: Page,
        url_pattern: str,
        status: int = 200,
        body: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> Iterator[None]:
        """
        Context manager for mocking API responses.

        Args:
            page: Playwright page instance
            url_pattern: URL pattern to intercept (glob or regex)
            status: HTTP status code to return
            body: Response body as dictionary (will be JSON encoded)
            headers: Response headers

        Example:
            with NetworkInterceptor.mock_api_response(
                page, "**/api/users/**", status=500
            ):
                page.goto("http://localhost:8080")
        """
        default_headers = {"Content-Type": "application/json"}
        if headers:
            default_headers.update(headers)

        default_body = body or {"error": "Mocked response"}

        def handler(route: Route) -> None:
            route.fulfill(
                status=status,
                body=json.dumps(default_body),
                headers=default_headers,
            )

        page.route(url_pattern, handler)
        try:
            yield
        finally:
            page.unroute(url_pattern)

    @staticmethod
    @contextmanager
    def mock_network_failure(
        page: Page,
        url_pattern: str,
        error: str = "failed",
    ) -> Iterator[None]:
        """
        Context manager for simulating network failures.

        Args:
            page: Playwright page instance
            url_pattern: URL pattern to intercept
            error: Error type ("failed", "aborted", "timedout", "accessdenied")

        Example:
            with NetworkInterceptor.mock_network_failure(
                page, "**/api/**", error="timedout"
            ):
                page.goto("http://localhost:8080")
        """

        def handler(route: Route) -> None:
            route.abort(error)

        page.route(url_pattern, handler)
        try:
            yield
        finally:
            page.unroute(url_pattern)

    @staticmethod
    @contextmanager
    def conditional_intercept(
        page: Page,
        url_pattern: str,
        condition: Callable[[Route], bool],
        handler: Callable[[Route], None],
    ) -> Iterator[None]:
        """
        Context manager for conditional request interception.

        Args:
            page: Playwright page instance
            url_pattern: URL pattern to intercept
            condition: Function that returns True if request should be intercepted
            handler: Function to handle intercepted requests

        Example:
            def is_post(route):
                return route.request.method == "POST"

            def return_error(route):
                route.fulfill(status=500)

            with NetworkInterceptor.conditional_intercept(
                page, "**/api/**", is_post, return_error
            ):
                page.goto("http://localhost:8080")
        """

        def router(route: Route) -> None:
            if condition(route):
                handler(route)
            else:
                route.continue_()

        page.route(url_pattern, router)
        try:
            yield
        finally:
            page.unroute(url_pattern)


class ResponseBuilder:
    """Builder for constructing mock responses."""

    def __init__(self) -> None:
        self.status: int = 200
        self.body: dict[str, Any] = {}
        self.headers: dict[str, str] = {"Content-Type": "application/json"}

    def with_status(self, status: int) -> "ResponseBuilder":
        """Set the HTTP status code."""
        self.status = status
        return self

    def with_body(self, body: dict[str, Any]) -> "ResponseBuilder":
        """Set the response body."""
        self.body = body
        return self

    def with_header(self, key: str, value: str) -> "ResponseBuilder":
        """Add a response header."""
        self.headers[key] = value
        return self

    def build(self) -> dict[str, Any]:
        """Build the response configuration."""
        return {
            "status": self.status,
            "body": json.dumps(self.body),
            "headers": self.headers,
        }
