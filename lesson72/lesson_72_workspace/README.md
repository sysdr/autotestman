# Lesson 72 — Jenkins & GitHub Actions CI workspace

This repository **is** the runnable project. After you **clone** it, work in the **repository root** (the folder that contains `Jenkinsfile`, `requirements.txt`, and `tests/`). **No parent `setup.py` or other generator is required** on your machine—everything you need is in this tree.

**Prerequisites:** Python **3.11+**, `git`. **Docker** is optional and only used if you run `cleanup.sh`.

## Contents

| Path | Purpose |
|------|---------|
| `Jenkinsfile` | Declarative pipeline: venv, lint, test, JUnit + artifacts |
| `.github/workflows/tests.yml` | Same flow on GitHub-hosted runners |
| `requirements.txt` | Pinned pytest stack |
| `tests/` | Config validation + sanity tests |
| `reports/` | Created at test time (`junit.xml`, HTML report) |
| `cleanup.sh` | Docker stop/prune + local cache cleanup |

## Quick start (local)

From the **root of the cloned repository**:

```bash
python3 -m venv .venv
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt
mkdir -p reports
./.venv/bin/pytest tests/ -v --junitxml=reports/junit.xml --html=reports/report.html --self-contained-html
```

On **PEP 668** systems (Debian/Ubuntu), always use a **virtualenv** as above; do not `pip install` into the system Python.

## CI

- **Jenkins:** create a Pipeline job from SCM; the repo root must contain this `Jenkinsfile`.
- **GitHub:** the workflow in `.github/workflows/tests.yml` runs on push and pull request when this tree is in your GitHub repository.

## Cleanup

From the repository root:

```bash
chmod +x cleanup.sh
./cleanup.sh
```

Stops running containers (when Docker is available), prunes unused Docker objects, and removes local `.venv` / caches under this project. May require **sudo** to stop the `docker` system service on some hosts.
