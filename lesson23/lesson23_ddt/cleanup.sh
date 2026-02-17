#!/bin/bash

# Cleanup Script for Docker and Project Files
# Stops all Docker containers and removes unused Docker resources, containers, and images.

set -e

echo "🧹 Starting cleanup process..."

# Stop all running Docker containers
echo "📦 Stopping all Docker containers..."
docker stop $(docker ps -aq) 2>/dev/null || echo "   No running containers to stop"

# Remove all stopped containers
echo "🗑️  Removing stopped containers..."
docker rm $(docker ps -aq) 2>/dev/null || echo "   No containers to remove"

# Remove unused Docker images
echo "🖼️  Removing unused Docker images..."
docker image prune -a -f 2>/dev/null || echo "   No unused images to remove"

# Remove unused Docker volumes
echo "💾 Removing unused Docker volumes..."
docker volume prune -f 2>/dev/null || echo "   No unused volumes to remove"

# Remove unused Docker networks
echo "🌐 Removing unused Docker networks..."
docker network prune -f 2>/dev/null || echo "   No unused networks to remove"

# Full Docker system cleanup (containers, networks, images, build cache, volumes)
echo "🧼 Performing full Docker system cleanup..."
docker system prune -a -f --volumes 2>/dev/null || echo "   Docker cleanup completed"

echo "✅ Docker cleanup completed!"

# Optional: project file cleanup (run from repo root or adjust paths)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="${SCRIPT_DIR%/*}"
echo "📁 Cleaning project files under ${ROOT}..."

find "$ROOT" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$ROOT" -type f -name "*.pyc" -delete 2>/dev/null || true
find "$ROOT" -type f -name "*.pyo" -delete 2>/dev/null || true
find "$ROOT" -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find "$ROOT" -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
find "$ROOT" -type d \( -name "venv" -o -name ".venv" \) -exec rm -rf {} + 2>/dev/null || true
find "$ROOT" -type d -name "istio" -exec rm -rf {} + 2>/dev/null || true
find "$ROOT" -type f \( -name "*.istio.yaml" -o -name "*.istio.yml" \) -delete 2>/dev/null || true

echo "✅ Project cleanup completed!"
echo "🎉 All cleanup operations finished successfully!"
