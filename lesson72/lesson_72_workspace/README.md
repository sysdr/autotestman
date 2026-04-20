# Lesson 72 — Jenkins & GitHub Actions CI workspace

This folder is a **small Python project** used to teach **declarative Jenkins pipelines** and **GitHub Actions** running **pytest** with JUnit and HTML reports.

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

```bash
cd lesson_72_workspace
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
./.venv/bin/pytest tests/ -v --junitxml=reports/junit.xml --html=reports/report.html --self-contained-html
```

On **PEP 668** systems (Debian/Ubuntu), always use a **virtualenv** as above; do not `pip install` into the system Python.

## CI

- **Jenkins:** create a Pipeline job from SCM; ensure the repo root contains this `Jenkinsfile`.
- **GitHub:** push this tree (or merge these paths into your repo); Actions runs on push/PR per `tests.yml`.

## Cleanup

From this directory:

```bash
chmod +x cleanup.sh
./cleanup.sh
```

Stops running containers (when Docker is available), prunes unused Docker objects, and removes local `venv` / caches. May require **sudo** to stop the `docker` system service on some hosts.
