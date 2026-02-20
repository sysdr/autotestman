#!/usr/bin/env bash
# cleanup.sh - Stop containers and remove unused Docker resources
# Usage: ./cleanup.sh
# Optional: pass --stop-daemon to also stop Docker service (requires sudo)

set -e

echo "=== Docker cleanup ==="

# Optional: stop Docker daemon (e.g. ./cleanup.sh --stop-daemon)
if [ "${1:-}" = "--stop-daemon" ]; then
  echo "Stopping Docker service..."
  sudo systemctl stop docker 2>/dev/null || true
  sudo systemctl stop docker.socket 2>/dev/null || true
fi

# Stop all running containers
echo "Stopping all running containers..."
docker stop $(docker ps -q 2>/dev/null) 2>/dev/null || true

# Remove all containers (running and stopped)
echo "Removing all containers..."
docker rm -f $(docker ps -aq 2>/dev/null) 2>/dev/null || true

# Remove unused images (dangling and optionally all unused)
echo "Removing unused images..."
docker image prune -af

# Remove unused volumes
echo "Removing unused volumes..."
docker volume prune -f

# Remove unused networks
echo "Removing unused networks..."
docker network prune -f

# Full system prune (containers, networks, images with no containers, build cache)
echo "System prune..."
docker system prune -af

echo "=== Docker cleanup done ==="
