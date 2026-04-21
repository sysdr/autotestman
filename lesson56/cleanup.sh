#!/usr/bin/env bash
set -euo pipefail

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

echo "[cleanup] Removing local caches..."
rm -rf .pytest_cache || true
find . -type d -name "__pycache__" -prune -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true

echo "[cleanup] Done."
