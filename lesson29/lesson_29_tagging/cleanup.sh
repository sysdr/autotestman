#!/usr/bin/env bash
#
# cleanup.sh - Stop containers and remove unused Docker resources.
#              Optionally remove node_modules, venv, .pytest_cache, .pyc, Istio files.
#
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=============================================="
echo "  Cleanup: Docker + project artifacts"
echo "=============================================="

# --- Docker: stop all containers ---
echo ""
echo "[1] Stopping all Docker containers..."
docker stop $(docker ps -aq) 2>/dev/null || true

# --- Docker: remove containers, networks, images, build cache ---
echo "[2] Removing stopped containers..."
docker container prune -f

echo "[3] Removing unused networks..."
docker network prune -f

echo "[4] Removing dangling images..."
docker image prune -f

echo "[5] Removing unused images (not just dangling)..."
docker image prune -a -f

echo "[6] Removing build cache..."
docker builder prune -f

echo "[7] Removing unused volumes..."
docker volume prune -f

# --- Project: remove common artifacts ---
echo ""
echo "[8] Removing project artifacts (node_modules, venv, .pytest_cache, .pyc, __pycache__, Istio)..."
find . -depth -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
find . -depth -type d -name "venv" -exec rm -rf {} + 2>/dev/null || true
find . -depth -type d -name ".venv" -exec rm -rf {} + 2>/dev/null || true
find . -depth -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find . -depth -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -depth -type d -name "istio-*" -exec rm -rf {} + 2>/dev/null || true
rm -rf ./istio 2>/dev/null || true

echo ""
echo "=============================================="
echo "  Cleanup finished."
echo "=============================================="
