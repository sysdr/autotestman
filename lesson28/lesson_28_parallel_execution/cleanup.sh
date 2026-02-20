#!/bin/bash
# Cleanup: stop Docker containers, remove unused Docker resources,
# and remove node_modules, venv, .pytest_cache, .pyc, Istio from project.
# Run from lesson28 or from repo root.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Clean from repo root (parent of lesson28) so entire project is cleaned
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🧹 Cleanup: Docker + project artifacts"
echo "   Project root: $PROJECT_ROOT"
echo ""

# --- Docker: stop service and containers ---
echo "📦 Stopping Docker containers..."
docker stop $(docker ps -aq) 2>/dev/null || echo "   No running containers"

echo "🗑️  Removing stopped containers..."
docker rm $(docker ps -aq) 2>/dev/null || echo "   No containers to remove"

echo "🖼️  Removing unused images..."
docker image prune -a -f 2>/dev/null || true

echo "💾 Removing unused volumes..."
docker volume prune -f 2>/dev/null || true

echo "🌐 Removing unused networks..."
docker network prune -f 2>/dev/null || true

echo "🧼 Full Docker system prune..."
docker system prune -a -f --volumes 2>/dev/null || true

# Optional: stop Docker daemon (uncomment if desired)
# echo "⏹️  Stopping Docker service..."
# sudo systemctl stop docker 2>/dev/null || true

echo "✅ Docker cleanup done"
echo ""

# --- Project: node_modules, venv, .pytest_cache, .pyc, Istio ---
echo "📁 Cleaning project artifacts under $PROJECT_ROOT..."

cd "$PROJECT_ROOT"

echo "   Removing node_modules..."
find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true

echo "   Removing venv / .venv..."
find . -type d \( -name "venv" -o -name ".venv" \) -exec rm -rf {} + 2>/dev/null || true

echo "   Removing .pytest_cache..."
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

echo "   Removing __pycache__..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

echo "   Removing .pyc / .pyo..."
find . -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete 2>/dev/null || true

echo "   Removing Istio files/dirs..."
find . -type f \( -name "*istio*" -o -name "*.istio.yaml" -o -name "*.istio.yml" \) -delete 2>/dev/null || true
find . -type d -name "istio" -exec rm -rf {} + 2>/dev/null || true

echo "✅ Project cleanup done"
echo ""
echo "🎉 Cleanup finished."
