#!/bin/bash
# Cleanup: stop Docker containers, remove unused Docker resources (containers, images, volumes, networks),
# then remove node_modules, venv, .venv, .pytest_cache, .pyc, __pycache__, and Istio files from the project.
# Run from playwright_lesson_31 or from repo root.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Clean lesson31 and its subdirs (playwright_lesson_31, etc.)
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🧹 Cleanup: Docker + project artifacts"
echo "   Project root: $PROJECT_ROOT"
echo ""

# --- Docker: stop containers and remove unused resources ---
echo "📦 Stopping Docker containers..."
docker stop $(docker ps -aq) 2>/dev/null || echo "   No running containers to stop"

echo "🗑️  Removing stopped containers..."
docker rm $(docker ps -aq) 2>/dev/null || echo "   No containers to remove"

echo "🖼️  Removing unused images..."
docker image prune -a -f 2>/dev/null || true

echo "💾 Removing unused volumes..."
docker volume prune -f 2>/dev/null || true

echo "🌐 Removing unused networks..."
docker network prune -f 2>/dev/null || true

echo "🧼 Full Docker system prune (all unused data)..."
docker system prune -a -f --volumes 2>/dev/null || true

# Optional: stop Docker daemon (uncomment to stop Docker service)
# echo "⏹️  Stopping Docker service..."
# sudo systemctl stop docker 2>/dev/null || true

echo "✅ Docker cleanup done"
echo ""

# --- Project: node_modules, venv, .pytest_cache, .pyc, Istio ---
echo "📁 Cleaning project artifacts under $PROJECT_ROOT..."
cd "$PROJECT_ROOT"

echo "   Removing .pyc / .pyo files..."
find . -type f \( -name "*.pyc" -o -name "*.pyo" \) -delete 2>/dev/null || true

echo "   Removing __pycache__ directories..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

echo "   Removing .pytest_cache..."
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

echo "   Removing node_modules..."
find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true

echo "   Removing venv / .venv..."
find . -type d \( -name "venv" -o -name ".venv" \) -exec rm -rf {} + 2>/dev/null || true

echo "   Removing Istio-related files and directories..."
find . -type f \( -name "*istio*" -o -name "*.istio.yaml" -o -name "*.istio.yml" \) -delete 2>/dev/null || true
find . -type d -name "istio" -exec rm -rf {} + 2>/dev/null || true

echo "✅ Project cleanup done"
echo ""
echo "🎉 Cleanup finished."
