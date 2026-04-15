#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

echo "[cleanup] Stopping Lesson 64 AUT on port 5001 (if any)..."
fuser -k 5001/tcp 2>/dev/null || true

echo "[cleanup] Stopping docker containers (if any)..."
if command -v docker >/dev/null 2>&1; then
  CONTAINERS="$(docker ps -q || true)"
  if [[ -n "${CONTAINERS}" ]]; then
    docker stop ${CONTAINERS} || true
  fi

  echo "[cleanup] Pruning unused docker resources..."
  docker container prune -f || true
  docker image prune -af || true
  docker volume prune -f || true
  docker network prune -f || true
  docker system prune -af || true
else
  echo "[cleanup] docker CLI not found; skipping docker cleanup."
fi

echo "[cleanup] Removing local caches under ${ROOT}..."
rm -rf .pytest_cache || true
find . -type d -name "__pycache__" -prune -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

echo "[cleanup] Done."
