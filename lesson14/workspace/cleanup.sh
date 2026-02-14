#!/bin/bash

# cleanup.sh - Cleanup script for Docker resources and project files
# This script stops containers and removes unused Docker resources

set -e

echo "=========================================="
echo "Starting Cleanup Process"
echo "=========================================="

# Stop all running containers
echo ""
echo "1. Stopping all Docker containers..."
if [ "$(docker ps -q)" ]; then
    docker stop $(docker ps -q)
    echo "   ✓ All running containers stopped"
else
    echo "   ℹ No running containers found"
fi

# Stop all containers (including stopped ones)
if [ "$(docker ps -aq)" ]; then
    docker stop $(docker ps -aq) 2>/dev/null || true
    echo "   ✓ All containers stopped"
fi

# Remove all stopped containers
echo ""
echo "2. Removing stopped containers..."
if [ "$(docker ps -aq)" ]; then
    docker rm $(docker ps -aq) 2>/dev/null || true
    echo "   ✓ Stopped containers removed"
else
    echo "   ℹ No containers to remove"
fi

# Remove unused images
echo ""
echo "3. Removing unused Docker images..."
docker image prune -af --filter "until=24h" 2>/dev/null || true
echo "   ✓ Unused images removed"

# Remove unused volumes
echo ""
echo "4. Removing unused Docker volumes..."
docker volume prune -af 2>/dev/null || true
echo "   ✓ Unused volumes removed"

# Remove unused networks
echo ""
echo "5. Removing unused Docker networks..."
docker network prune -f 2>/dev/null || true
echo "   ✓ Unused networks removed"

# System prune (optional - removes all unused data)
echo ""
echo "6. Performing Docker system prune..."
docker system prune -af --volumes 2>/dev/null || true
echo "   ✓ Docker system cleanup completed"

# Show remaining resources
echo ""
echo "=========================================="
echo "Cleanup Summary"
echo "=========================================="
echo "Containers: $(docker ps -aq | wc -l)"
echo "Images: $(docker images -q | wc -l)"
echo "Volumes: $(docker volume ls -q | wc -l)"
echo "Networks: $(docker network ls -q | wc -l)"
echo ""
echo "✓ Cleanup completed successfully!"
echo "=========================================="
