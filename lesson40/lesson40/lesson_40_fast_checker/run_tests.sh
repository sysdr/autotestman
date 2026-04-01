#!/usr/bin/env bash
# Run tests with this project's venv (pytest 8.1.2 + pytest-asyncio 0.23.8).
# Use this so the correct versions are used even if another venv is active.
set -e
cd "$(dirname "$0")"
VENV="automation-venv"
if [[ ! -d "$VENV" ]]; then
  echo "Creating $VENV and installing dependencies..."
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -r requirements.txt
  "$VENV/bin/playwright" install chromium
fi
"$VENV/bin/python" -m pytest "$@"
