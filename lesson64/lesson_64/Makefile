# Use the lesson venv so `make test` matches setup.py (bare `pytest` often does not).
.PHONY: test aut
test:
	.venv/bin/python -m pytest tests/ -v --tb=short

aut:
	.venv/bin/python app/server.py
