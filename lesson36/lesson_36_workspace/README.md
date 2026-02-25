# Lesson 36: Authenticated State Storage

## Overview

This workspace demonstrates the production pattern for authentication caching in Playwright tests using the `storage_state` API.

## The Problem

Naive test suites authenticate for EVERY test:
- 100 tests × 3 seconds = 5 minutes wasted
- Rate limiting on auth endpoints
- Flaky tests due to network issues

## The Solution

Authenticate ONCE, save the state, reuse for all tests:
- 1 authentication + 100 instant loads = 8 seconds total
- 97% time reduction
- Zero auth server load

## Architecture

```
Session Fixture (scope="session")
  ↓
Authenticate & Save State (runs once)
  ↓
auth_state.json (persistent cache)
  ↓
Function Fixtures (scope="function")
  ↓
Load State into Context (per test)
  ↓
Tests Execute (already authenticated)
```

## File Structure

```
lesson_36_workspace/
├── conftest.py              # Pytest fixtures with storage_state logic
├── pages/
│   ├── base_page.py         # Base page object
│   └── dashboard_page.py    # Dashboard page object
├── tests/
│   └── test_authenticated_state.py
├── auth_state.json          # Generated on first run
├── verify_implementation.py # Verification script
└── README.md
```

## Quick Start

### 1. Install Dependencies

```bash
pip install playwright pytest
playwright install chromium
```

### 2. Run Tests

```bash
cd lesson_36_workspace
pytest tests/ -v -s
```

**First Run:**
- Executes authentication flow
- Saves state to `auth_state.json`
- Runs all tests with loaded state

**Subsequent Runs:**
- Skips authentication
- Loads cached state instantly
- Tests execute immediately

### 3. Verify Implementation

```bash
python verify_implementation.py
```

## Key Files Explained

### `conftest.py`

**`authenticated_state_file` (session-scoped):**
- Runs ONCE per test session
- Checks if `auth_state.json` exists
- If not, authenticates and saves state
- Returns path to state file

**`authenticated_context` (function-scoped):**
- Runs for EACH test
- Creates browser context with `storage_state` parameter
- Playwright injects cookies + localStorage automatically

**`authenticated_page` (function-scoped):**
- Convenience fixture
- Returns a page with auth already loaded

### `auth_state.json`

Example structure:

```json
{
  "cookies": [
    {
      "name": "session_id",
      "value": "abc123xyz789",
      "domain": "demo.playwright.dev",
      "path": "/",
      "httpOnly": false,
      "secure": false
    }
  ],
  "origins": [
    {
      "origin": "https://demo.playwright.dev",
      "localStorage": [
        {"name": "auth_token", "value": "demo_token_xyz_123"},
        {"name": "user_id", "value": "42"}
      ]
    }
  ]
}
```

## Production Patterns

### Multi-User Testing

```python
@pytest.fixture(scope="session")
def admin_state(browser):
    return authenticate_as("admin@example.com")

@pytest.fixture(scope="session")
def user_state(browser):
    return authenticate_as("user@example.com")
```

### Token Refresh

```python
@pytest.fixture(scope="session", autouse=True)
def refresh_state_daily():
    state_file = Path("auth_state.json")
    if state_file.exists():
        age = time.time() - state_file.stat().st_mtime
        if age > 86400:  # 24 hours
            state_file.unlink()  # Force re-authentication
```

## Performance Comparison

| Scenario | Naive Approach | Storage State |
|----------|---------------|---------------|
| 10 tests | 30s | 4s |
| 100 tests | 300s | 8s |
| 500 tests | 1500s (25min) | 28s |

## Next Steps

- Lesson 37: Multi-Role Authentication (Admin, User, Guest)
- Lesson 38: API-Based State Setup (Skip UI for speed)
- Lesson 39: Parallel Test Execution with Shared State

---

**Engineering Principle:** Authentication is a side effect, not the behavior under test. Isolate it.