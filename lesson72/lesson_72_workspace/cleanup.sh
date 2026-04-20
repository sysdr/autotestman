#!/usr/bin/env bash
# Lesson 72 — stop Docker workloads, prune unused images/containers, clear local caches.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

LESSON_DIR="$(cd "${ROOT}/.." && pwd)"

echo "[cleanup] Lesson 72 — workspace: ${ROOT}"
echo "[cleanup] Lesson directory (parent): ${LESSON_DIR}"

echo "[cleanup] Stopping Docker containers (if any)..."
if command -v docker >/dev/null 2>&1; then
  if docker info >/dev/null 2>&1; then
    CONTAINERS="$(docker ps -q 2>/dev/null || true)"
    if [[ -n "${CONTAINERS}" ]]; then
      docker stop ${CONTAINERS} || true
    fi
    echo "[cleanup] docker compose down (if compose project present)..."
    (cd "$ROOT" && docker compose down --remove-orphans 2>/dev/null) || true

    echo "[cleanup] Pruning unused Docker resources..."
    docker container prune -f || true
    docker image prune -af || true
    docker volume prune -f || true
    docker network prune -f || true
    docker builder prune -af || true
    docker system prune -af || true
  else
    echo "[cleanup] Docker daemon not reachable; skipping container/image prune."
  fi
else
  echo "[cleanup] docker CLI not found; skipping Docker steps."
fi

echo "[cleanup] Stopping docker service (optional; may require sudo)..."
if command -v systemctl >/dev/null 2>&1; then
  systemctl stop docker 2>/dev/null || sudo -n systemctl stop docker 2>/dev/null || true
fi
if command -v service >/dev/null 2>&1; then
  service docker stop 2>/dev/null || true
fi

echo "[cleanup] Removing node_modules, virtualenvs, Istio paths, pytest caches, bytecode..."
find "$ROOT" -type d -name "node_modules" -prune -exec rm -rf {} + 2>/dev/null || true
find "$ROOT" -type d \( -name ".venv" -o -name "venv" -o -name "ENV" -o -name "env" \) -prune -exec rm -rf {} + 2>/dev/null || true
find "$ROOT" -type d -name "istio" -prune -exec rm -rf {} + 2>/dev/null || true
find "$ROOT" -type f \( -name "*.istio.yaml" -o -name "*.istio.yml" \) -delete 2>/dev/null || true
rm -rf "$ROOT"/.pytest_cache 2>/dev/null || true
find "$ROOT" -type d -name ".pytest_cache" -prune -exec rm -rf {} + 2>/dev/null || true
find "$ROOT" -type d -name "__pycache__" -prune -exec rm -rf {} + 2>/dev/null || true
find "$ROOT" -type f -name "*.pyc" -delete 2>/dev/null || true

echo "[cleanup] Lesson-level caches under ${LESSON_DIR} (pytest, bytecode only)..."
rm -rf "${LESSON_DIR}/.pytest_cache" 2>/dev/null || true
find "${LESSON_DIR}" -maxdepth 3 -type d -name "__pycache__" -prune -exec rm -rf {} + 2>/dev/null || true
find "${LESSON_DIR}" -maxdepth 4 -type f -name "*.pyc" -delete 2>/dev/null || true
find "${LESSON_DIR}" -maxdepth 3 -type d -name "node_modules" -prune -exec rm -rf {} + 2>/dev/null || true
find "${LESSON_DIR}" -maxdepth 3 -type d \( -name ".venv" -o -name "venv" \) -prune -exec rm -rf {} + 2>/dev/null || true
find "${LESSON_DIR}" -maxdepth 3 -type d -name "istio" -prune -exec rm -rf {} + 2>/dev/null || true
find "${LESSON_DIR}" -maxdepth 3 -type f \( -name "*.istio.yaml" -o -name "*.istio.yml" \) -delete 2>/dev/null || true

echo "[cleanup] Done."
