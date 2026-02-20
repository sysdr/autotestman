#!/bin/bash
# Cleanup: stop Docker containers, remove unused Docker resources,
# and remove node_modules, venv, .pytest_cache, .pyc, Istio files from this project.

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🧹 Cleanup starting in: $SCRIPT_DIR"
echo ""

# --- Docker: stop containers ---
echo "📦 Stopping all Docker containers..."
docker stop $(docker ps -aq) 2>/dev/null || echo "   (no running containers)"

# --- Docker: remove stopped containers ---
echo "🗑️  Removing stopped containers..."
docker rm $(docker ps -aq) 2>/dev/null || echo "   (no containers to remove)"

# --- Docker: remove unused images ---
echo "🖼️  Removing unused Docker images..."
docker image prune -a -f 2>/dev/null || true

# --- Docker: remove unused volumes ---
echo "💾 Removing unused Docker volumes..."
docker volume prune -f 2>/dev/null || true

# --- Docker: remove unused networks ---
echo "🌐 Removing unused Docker networks..."
docker network prune -f 2>/dev/null || true

# --- Docker: full system prune (optional, aggressive) ---
echo "🧼 Docker system prune..."
docker system prune -a -f --volumes 2>/dev/null || true

echo "✅ Docker cleanup done."
echo ""

# --- Project: node_modules ---
echo "📁 Removing node_modules..."
find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true

# --- Project: venv / .venv ---
echo "📁 Removing venv / .venv..."
find . -type d \( -name "venv" -o -name ".venv" \) -exec rm -rf {} + 2>/dev/null || true

# --- Project: .pytest_cache ---
echo "📁 Removing .pytest_cache..."
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

# --- Project: .pyc and __pycache__ ---
echo "📁 Removing .pyc and __pycache__..."
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# --- Project: Istio ---
echo "📁 Removing Istio files/dirs..."
find . -type f \( -name "*.istio.yaml" -o -name "*.istio.yml" \) -delete 2>/dev/null || true
find . -type d -name "istio" -exec rm -rf {} + 2>/dev/null || true
find . -type f -path "*istio*" -delete 2>/dev/null || true

echo "✅ Project cleanup done."
echo ""
echo "🎉 Cleanup finished."
