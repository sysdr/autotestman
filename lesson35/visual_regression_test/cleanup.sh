#!/bin/bash
#
# Cleanup: stop Docker containers and remove unused Docker resources,
# then remove project cruft (node_modules, venv, .pytest_cache, .pyc, Istio).
# Run from lesson35 or project root.
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🧹 Cleanup (project root: $SCRIPT_DIR)"
echo ""

# --- Docker: stop containers and remove unused resources ---
echo "📦 Docker: stopping all containers..."
docker stop $(docker ps -aq) 2>/dev/null || echo "   (no running containers)"

echo "🗑️  Docker: removing stopped containers..."
docker rm $(docker ps -aq) 2>/dev/null || echo "   (none to remove)"

echo "🖼️  Docker: removing unused images..."
docker image prune -a -f 2>/dev/null || true

echo "💾 Docker: removing unused volumes..."
docker volume prune -f 2>/dev/null || true

echo "🌐 Docker: removing unused networks..."
docker network prune -f 2>/dev/null || true

echo "🧼 Docker: system prune (all unused build cache, etc.)..."
docker system prune -a -f --volumes 2>/dev/null || true

echo "✅ Docker cleanup done."
echo ""

# --- Project: remove generated/cache/ignored artifacts ---
echo "📁 Project cleanup..."

echo "   Removing .pytest_cache..."
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

echo "   Removing __pycache__ and .pyc / .pyo..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true

echo "   Removing node_modules..."
find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true

echo "   Removing venv / .venv..."
find . -type d -name "venv" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".venv" -exec rm -rf {} + 2>/dev/null || true

echo "   Removing Istio-related files/dirs..."
find . -type f -name "*istio*" -delete 2>/dev/null || true
find . -type d -name "*istio*" -exec rm -rf {} + 2>/dev/null || true

echo "✅ Project cleanup done."
echo ""
echo "🎉 Cleanup finished."
