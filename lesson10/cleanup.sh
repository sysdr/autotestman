#!/bin/bash
# Docker Cleanup Script
# Stops all containers and removes unused Docker resources

set -e

echo "=========================================="
echo "Docker Cleanup Script"
echo "=========================================="
echo ""

# Stop all running containers
echo "Stopping all running containers..."
if [ "$(docker ps -q)" ]; then
    docker stop $(docker ps -q)
    echo "✓ All running containers stopped"
else
    echo "✓ No running containers found"
fi

# Remove all stopped containers
echo ""
echo "Removing all stopped containers..."
if [ "$(docker ps -a -q)" ]; then
    docker rm $(docker ps -a -q)
    echo "✓ All containers removed"
else
    echo "✓ No containers to remove"
fi

# Remove unused images
echo ""
echo "Removing unused Docker images..."
docker image prune -a -f
echo "✓ Unused images removed"

# Remove unused volumes
echo ""
echo "Removing unused Docker volumes..."
docker volume prune -f
echo "✓ Unused volumes removed"

# Remove unused networks
echo ""
echo "Removing unused Docker networks..."
docker network prune -f
echo "✓ Unused networks removed"

# System prune (removes all unused data)
echo ""
echo "Performing system-wide cleanup..."
docker system prune -a -f --volumes
echo "✓ System-wide cleanup complete"

echo ""
echo "=========================================="
echo "✓ Docker cleanup completed successfully!"
echo "=========================================="
