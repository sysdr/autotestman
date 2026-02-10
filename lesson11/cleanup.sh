#!/bin/bash
# Cleanup script for Docker resources and containers

set -e

echo "=========================================="
echo "Docker Cleanup Script"
echo "=========================================="

# Stop all running containers
echo "[1/5] Stopping all running containers..."
docker stop $(docker ps -q) 2>/dev/null || echo "No running containers to stop"

# Remove all stopped containers
echo "[2/5] Removing all stopped containers..."
docker rm $(docker ps -aq) 2>/dev/null || echo "No stopped containers to remove"

# Remove unused images
echo "[3/5] Removing unused Docker images..."
docker image prune -af --filter "until=24h" 2>/dev/null || echo "No unused images to remove"

# Remove unused volumes
echo "[4/5] Removing unused Docker volumes..."
docker volume prune -af 2>/dev/null || echo "No unused volumes to remove"

# Remove unused networks
echo "[5/5] Removing unused Docker networks..."
docker network prune -af 2>/dev/null || echo "No unused networks to remove"

# System prune (optional - removes everything unused)
echo "[BONUS] Running Docker system prune..."
docker system prune -af --volumes 2>/dev/null || echo "System prune completed"

echo ""
echo "=========================================="
echo "Docker cleanup completed!"
echo "=========================================="
echo ""
echo "Summary:"
docker system df 2>/dev/null || echo "Docker not available"
