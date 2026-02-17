#!/bin/bash
# Cleanup script: stop containers, remove unused Docker resources, containers, images.
# Optionally stops Docker service (edit below if needed).

set -e

echo "=========================================="
echo "🧹 Docker cleanup"
echo "=========================================="

# Stop all running containers (safe when none exist)
echo "📦 Stopping all Docker containers..."
docker ps -q 2>/dev/null | xargs -r docker stop 2>/dev/null || true
echo "   Done."

# Docker Compose down (project dir or current dir)
for f in docker-compose.yml docker-compose.yaml; do
  if [ -f "$f" ]; then
    echo "📦 Bringing down Docker Compose stack..."
    docker compose -f "$f" down 2>/dev/null || docker-compose -f "$f" down 2>/dev/null || true
    echo "   Done."
    break
  fi
done

# Remove stopped containers
echo "🗑️  Removing stopped containers..."
docker ps -aq 2>/dev/null | xargs -r docker rm -f 2>/dev/null || true
echo "   Done."

# Remove unused images
echo "🖼️  Removing unused Docker images..."
docker image prune -a -f 2>/dev/null || true
echo "   Done."

# Remove unused volumes
echo "💾 Removing unused Docker volumes..."
docker volume prune -f 2>/dev/null || true
echo "   Done."

# Remove unused networks
echo "🌐 Removing unused Docker networks..."
docker network prune -f 2>/dev/null || true
echo "   Done."

# Full system prune (all unused build cache, etc.)
echo "🧼 Docker system prune..."
docker system prune -a -f --volumes 2>/dev/null || true
echo "   Done."

# Optional: stop Docker daemon (uncomment if you want to stop the service)
# echo "🛑 Stopping Docker service..."
# sudo systemctl stop docker 2>/dev/null || echo "   (skip or permission denied)"

echo "=========================================="
echo "✅ Docker cleanup complete"
echo "=========================================="
