#!/usr/bin/env bash
#
# cleanup.sh - Stop Docker containers and remove unused Docker resources
# Usage: ./cleanup.sh
#

set -e

echo "=== Docker cleanup ==="

# Stop all running containers
echo "Stopping all running containers..."
docker stop $(docker ps -q) 2>/dev/null || true

# Stop docker compose if present
if [ -f "docker-compose.yml" ] || [ -f "docker-compose.yaml" ]; then
    echo "Stopping docker compose..."
    docker compose down 2>/dev/null || docker-compose down 2>/dev/null || true
fi

# Remove all stopped containers
echo "Removing stopped containers..."
docker container prune -f

# Remove unused images (dangling and optionally all unused)
echo "Removing dangling images..."
docker image prune -f

# Remove unused volumes
echo "Removing unused volumes..."
docker volume prune -f

# Remove unused networks
echo "Removing unused networks..."
docker network prune -f

# Optional: remove all unused images (not just dangling)
# Uncomment the next line for more aggressive cleanup
# docker image prune -a -f

echo "=== Docker cleanup complete ==="
