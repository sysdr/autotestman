#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
PY="$ROOT/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "Missing $ROOT/.venv — from the lesson64 folder run: python3 setup.py" >&2
  exit 1
fi
exec "$PY" "$ROOT/app/server.py"
