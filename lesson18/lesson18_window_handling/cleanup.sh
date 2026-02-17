#!/bin/bash
# Cleanup script for Docker containers and resources
# This script stops all containers and removes unused Docker resources
# (containers, images, volumes, networks, build cache)

set -e  # Exit on error

echo "=========================================="
echo "Docker Cleanup Script"
echo "=========================================="

# Ensure Docker is available
if ! command -v docker &>/dev/null; then
    echo "Docker is not installed or not in PATH. Exiting."
    exit 1
fi

# Stop all running containers
echo ""
echo "Step 1: Stopping all running containers..."
CONTAINERS=$(docker ps -q 2>/dev/null)
if [ -n "$CONTAINERS" ]; then
    docker stop $CONTAINERS
    echo "✓ Stopped all running containers"
else
    echo "✓ No running containers found"
fi

# Remove all stopped containers
echo ""
echo "Step 2: Removing all stopped containers..."
STOPPED=$(docker ps -aq 2>/dev/null)
if [ -n "$STOPPED" ]; then
    docker rm $STOPPED
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

# Remove build cache
echo ""
echo "Step 6: Removing unused build cache..."
docker builder prune -f 2>/dev/null || true
echo "✓ Removed unused build cache"

# Comprehensive system prune (optional; uncomment to remove all unused data)
# echo ""
# echo "Step 7: Comprehensive cleanup..."
# docker system prune -a -f --volumes
# echo "✓ Completed comprehensive cleanup"

echo ""
echo "=========================================="
echo "Docker cleanup completed successfully!"
echo "=========================================="
