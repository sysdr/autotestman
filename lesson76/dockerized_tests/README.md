# Lesson 76 — Dockerized Selenium tests (UQAP)

Headless **Chrome** + **pytest** + **pytest-html**, runnable **locally** (with Chrome installed) or **inside Docker** (image includes Chrome; Selenium Manager supplies a matching driver in the container).

There are **no API keys** or cloud credentials in this repository. Network tests use public URLs (e.g. `example.com`).

---

## Prerequisites

- **Docker** (optional, for containerized runs): Docker Engine / Docker Desktop with the daemon running.
- **Python 3.11+** (local runs): recommended **`.venv`** in this directory.
- **Google Chrome** or **Chromium** on the host for local pytest (not required if you only use Docker).

---

## Project layout

| Path | Purpose |
|------|---------|
| `Dockerfile` | Python 3.11 (Bookworm) + Chrome + test dependencies. |
| `requirements.txt` | Pinned Selenium / pytest stack. |
| `pytest.ini` | Keeps pytest `rootdir` anchored to this folder in monorepos. |
| `conftest.py` | Session-scoped Chrome driver; Docker vs local driver resolution. |
| `tests/` | Smoke tests (network, DOM, screenshots). |
| `utils/verify_result.py` | Parses `reports/report.html` after a Docker run. |
| `run_tests.sh` | Build image, run container with mounted `reports/`, verify. |
| `cleanup.sh` | Stop containers, prune Docker, remove caches / venv / optional Istio paths. |

---

## Local install and pytest

```bash
cd dockerized_tests   # or clone root if this folder is your repo root
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python -m pytest tests/ -v --tb=short
```

Override the browser binary if needed:

```bash
export CHROME_BIN=/path/to/google-chrome
./.venv/bin/python -m pytest tests/ -v
```

---

## Docker build and run

From this directory:

```bash
./run_tests.sh
```

Or manually:

```bash
docker build -t uqap-tests:lesson76 .
mkdir -p reports
docker run --rm -v "$(pwd)/reports:/app/reports" uqap-tests:lesson76
python3 utils/verify_result.py
```

Open `reports/report.html` in a browser.

---

## Cleanup

**Warning:** stops **all** running containers when Docker is available, prunes unused Docker objects, and may stop the **docker** service (best effort; may need `sudo`). Also deletes `.venv`, caches, and common junk under this folder and shallow paths under the parent `lesson76/` directory.

```bash
./cleanup.sh
```

---

## HTML report as metrics

There is no separate metrics server. After a run, **pytest-html** summary lines in `reports/report.html` show passed/failed counts; `utils/verify_result.py` prints the same for CI-style gates.
