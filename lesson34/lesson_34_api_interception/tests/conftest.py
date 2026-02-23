"""Pytest configuration and fixtures for API interception tests."""

import nest_asyncio

# Allow nested event loops so pytest-asyncio works with pytest-playwright
nest_asyncio.apply()
