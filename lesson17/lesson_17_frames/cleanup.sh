#!/bin/bash

# Cleanup script for Docker resources
# This script stops containers and removes unused Docker resources

set -e  # Exit on error

echo "=========================================="
echo "Docker Cleanup Script"
echo "=========================================="

# Stop all running containers
echo ""
echo "1. Stopping all running containers..."
RUNNING_CONTAINERS=$(docker ps -q)
if [ -z "$RUNNING_CONTAINERS" ]; then
    echo "   ✓ No running containers found"
else
    docker stop $RUNNING_CONTAINERS
    echo "   ✓ Stopped $(echo $RUNNING_CONTAINERS | wc -w) container(s)"
fi

# Remove all stopped containers
echo ""
echo "2. Removing stopped containers..."
STOPPED_CONTAINERS=$(docker ps -aq)
if [ -z "$STOPPED_CONTAINERS" ]; then
    echo "   ✓ No stopped containers found"
else
    docker rm $STOPPED_CONTAINERS 2>/dev/null || echo "   ⚠ Some containers could not be removed (may be in use)"
    echo "   ✓ Cleaned up stopped containers"
fi

# Remove unused images
echo ""
echo "3. Removing unused Docker images..."
docker image prune -f
echo "   ✓ Removed unused images"

# Remove unused volumes
echo ""
echo "4. Removing unused Docker volumes..."
docker volume prune -f
echo "   ✓ Removed unused volumes"

# Remove unused networks
echo ""
echo "5. Removing unused Docker networks..."
docker network prune -f
echo "   ✓ Removed unused networks"

# System prune (optional - removes all unused resources)
echo ""
echo "6. Performing system-wide cleanup..."
docker system prune -f
echo "   ✓ System cleanup completed"

# Show remaining resources
echo ""
echo "=========================================="
echo "Cleanup Summary"
echo "=========================================="
echo "Remaining containers: $(docker ps -aq | wc -l)"
echo "Remaining images: $(docker images -q | wc -l)"
echo ""
echo "✓ Cleanup completed successfully!"
