#!/bin/bash

# Cleanup script to stop containers and remove unused Docker resources

set -e

echo "=========================================="
echo "Docker Cleanup Script"
echo "=========================================="

# Stop all running containers
echo "Stopping all running containers..."
if docker ps -q | grep -q .; then
    docker stop $(docker ps -q)
    echo "✓ All containers stopped"
else
    echo "✓ No running containers found"
fi

# Remove all stopped containers
echo "Removing all stopped containers..."
if docker ps -aq | grep -q .; then
    docker rm $(docker ps -aq)
    echo "✓ All containers removed"
else
    echo "✓ No containers to remove"
fi

# Remove unused images
echo "Removing unused Docker images..."
docker image prune -a -f
echo "✓ Unused images removed"

# Remove unused volumes
echo "Removing unused Docker volumes..."
docker volume prune -f
echo "✓ Unused volumes removed"

# Remove unused networks
echo "Removing unused Docker networks..."
docker network prune -f
echo "✓ Unused networks removed"

# System prune (removes all unused data)
echo "Performing system-wide cleanup..."
docker system prune -a -f --volumes
echo "✓ System cleanup completed"

echo "=========================================="
echo "Docker cleanup completed successfully!"
echo "=========================================="
