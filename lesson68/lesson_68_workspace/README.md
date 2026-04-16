# Lesson 68 — Reporting in BDD (workspace)

This directory is the **runnable BDD project** (Gherkin features, steps, hooks, mock auth, HTML report).

No third-party **API keys** are used. Credentials in features are **lesson-only demos**.

## Prerequisites

- Python **3.11+** (3.12 OK)

## Bootstrap (generator in parent folder)

From the parent **`lesson68/`** directory (repository path `.../lesson68/`):

```bash
python3 setup.py
```

That (re)creates/refreshes this workspace, installs dependencies into **`.venv`**, runs the BDD suite, and writes **`reports/cucumber_report.html`**.

## Run tests manually

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python -m pytest steps/ -v --tb=short
```

Use the interpreter under **`.venv`** so `pytest-bdd` resolves correctly.

## View the report

Open **`reports/cucumber_report.html`** in a browser after a successful test run.

## Cleanup

Stops Docker containers (if Docker is available), prunes unused Docker objects, and removes **`node_modules`**, **`.venv` / `venv`**, **`.pytest_cache`**, **`__pycache__`**, **`*.pyc`**, and **Istio**-named paths under this workspace:

```bash
./cleanup.sh
```

## Implementation guide

See **`../IMPLEMENTATION_GUIDE.md`** in the parent folder (`lesson68/`, article-oriented).

## Layout

| Path | Role |
|------|------|
| `features/` | `.feature` files |
| `steps/` | Step definitions + `scenarios(...)` |
| `conftest.py` | pytest hooks; drives HTML report generation |
| `utils/bdd_reporter.py` | HTML report builder |
| `utils/auth_service.py` | In-memory mock auth |
| `requirements.txt` | pytest / pytest-bdd pins |
