#!/usr/bin/env bash
# Lesson 36 workspace cleanup: stop Docker, remove unused resources, local caches

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== Stopping Docker containers ==="
docker ps -q | xargs -r docker stop 2>/dev/null || true
docker compose down 2>/dev/null || true

echo "=== Removing unused Docker resources ==="
docker container prune -f
docker image prune -af
docker network prune -f
docker volume prune -f
docker system prune -af --volumes 2>/dev/null || true

echo "=== Removing local caches and generated files (workspace only) ==="
rm -rf .pytest_cache
rm -rf __pycache__
rm -rf pages/__pycache__
rm -rf tests/__pycache__
find . -type f -name "*.pyc" -delete
find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".venv" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "venv" -exec rm -rf {} + 2>/dev/null || true

echo "=== Cleanup complete ==="
