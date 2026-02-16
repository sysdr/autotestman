#!/bin/bash
# Cleanup script for Docker containers and resources
# This script stops all containers and removes unused Docker resources

set -e  # Exit on error

echo "=========================================="
echo "Docker Cleanup Script"
echo "=========================================="

# Stop all running containers
echo ""
echo "Step 1: Stopping all running containers..."
if [ "$(docker ps -q)" ]; then
    docker stop $(docker ps -q)
    echo "✓ Stopped all running containers"
else
    echo "✓ No running containers found"
fi

# Remove all stopped containers
echo ""
echo "Step 2: Removing all stopped containers..."
if [ "$(docker ps -aq)" ]; then
    docker rm $(docker ps -aq)
    echo "✓ Removed all stopped containers"
else
    echo "✓ No stopped containers found"
fi

# Remove unused images
echo ""
echo "Step 3: Removing unused Docker images..."
docker image prune -a -f
echo "✓ Removed unused images"

# Remove unused volumes
echo ""
echo "Step 4: Removing unused volumes..."
docker volume prune -f
echo "✓ Removed unused volumes"

# Remove unused networks
echo ""
echo "Step 5: Removing unused networks..."
docker network prune -f
echo "✓ Removed unused networks"

# Remove all unused resources (comprehensive cleanup)
echo ""
echo "Step 6: Comprehensive cleanup of all unused resources..."
docker system prune -a -f --volumes
echo "✓ Completed comprehensive cleanup"

echo ""
echo "=========================================="
echo "Docker cleanup completed successfully!"
echo "=========================================="
