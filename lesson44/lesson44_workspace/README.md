# Lesson 44 — Chaining Requests

Workspace for **UQAP** (Unified Quality Assurance Platform): testing API request chaining — create user, use returned ID in subsequent requests, no hardcoded IDs.

## What this does

- Runs a local FastAPI server with an in-memory user store (`server/app.py`).
- Tests use `utils/api_client.py` to create users, fetch by ID (from the create response), and delete. User IDs are never hardcoded; they flow through fixture chaining.

## Prerequisites

- Python 3.10+
- pip

## Setup

From this directory (`lesson44_workspace`):

```bash
pip install -r requirements.txt
```

Or use a virtual environment:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Run the project (no setup script)

Run both commands from **this directory** (`lesson44_workspace`) so `server` and `utils` resolve.

**1. Start the server** (in one terminal):

```bash
uvicorn server.app:app --host 0.0.0.0 --port 8000
```

(With venv: `.venv/bin/python -m uvicorn server.app:app --host 0.0.0.0 --port 8000`)

**2. Run tests** (in another terminal, from this directory):

```bash
pytest tests/test_user_chain.py -v
```

(With venv: `.venv/bin/python -m pytest tests/test_user_chain.py -v`)

The project is independent of any parent `setup.sh` or `setup.py`; install deps, start the server, then run pytest.

## Structure

- `server/app.py` — FastAPI app: POST/GET/DELETE `/users`, GET `/health`.
- `utils/api_client.py` — Typed HTTP client and `UserResponse` for chaining.
- `tests/conftest.py` — Session `api_client`, function-scoped `created_user` fixture.
- `tests/test_user_chain.py` — Tests: create → get by ID → delete → 404.
