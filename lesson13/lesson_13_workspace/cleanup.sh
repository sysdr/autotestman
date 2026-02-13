#!/bin/bash

# cleanup.sh
# Script to stop containers and remove unused Docker resources

set -e

echo "=========================================="
echo "Starting cleanup process..."
echo "=========================================="

# Stop all running containers
echo ""
echo "1. Stopping all running Docker containers..."
docker ps -q | xargs -r docker stop 2>/dev/null || echo "   No running containers found"

# Remove all stopped containers
echo ""
echo "2. Removing stopped containers..."
docker container prune -f || echo "   No stopped containers to remove"

# Remove unused images
echo ""
echo "3. Removing unused Docker images..."
docker image prune -a -f || echo "   No unused images to remove"

# Remove unused volumes
echo ""
echo "4. Removing unused volumes..."
docker volume prune -f || echo "   No unused volumes to remove"

# Remove unused networks
echo ""
echo "5. Removing unused networks..."
docker network prune -f || echo "   No unused networks to remove"

# System prune (removes all unused data)
echo ""
echo "6. Performing system-wide cleanup..."
docker system prune -a -f --volumes || echo "   System cleanup completed"

echo ""
echo "=========================================="
echo "Cleanup completed successfully!"
echo "=========================================="
