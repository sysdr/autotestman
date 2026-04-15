# Lesson 64 — Background & Hooks (BDD + Playwright)

Flask **Application Under Test (AUT)** on port **5001**, Gherkin features with **Background**,
and pytest fixtures in **`conftest.py`** (session browser + per-test context).

## Prerequisites

- Python 3.11+ (3.12 OK)
- No third-party **API keys** are required; the AUT uses in-memory demo users only.

## Bootstrap (recommended)

From the parent folder `lesson64/`:

```bash
python3 setup.py
```

That creates/refreshes this directory, installs dependencies into **`.venv`**, runs the BDD suite,
and writes **`lesson_64_report.html`**.

## Run manually

Terminal A — AUT:

```bash
./startup.sh
```

Terminal B — tests (must use the venv, not global `pytest`):

```bash
./run_tests.sh
# or: make test
# or: .venv/bin/python -m pytest tests/
```

Optional: `export LESSON64_FLASK_SECRET_KEY='your-dev-secret'` before starting the AUT.

## Cleanup

Stops Docker containers, prunes unused Docker objects, frees port **5001**, and removes
**`.pytest_cache`** / **`__pycache__`** / **`*.pyc`** under this folder:

```bash
./cleanup.sh
```

To remove the virtualenv as well: `rm -rf .venv`

## Layout

- `app/server.py` — Flask AUT
- `features/login.feature` — Gherkin + Background
- `tests/conftest.py` — Playwright fixtures (hooks)
- `tests/step_defs/test_login_steps.py` — step definitions
- `requirements.txt` — Python dependencies
