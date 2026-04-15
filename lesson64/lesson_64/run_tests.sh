#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
PY="$ROOT/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "Missing $ROOT/.venv — run setup.py first." >&2
  exit 1
fi
exec "$PY" -m pytest tests/ -v --tb=short "$@"
