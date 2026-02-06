#!/bin/bash

# Docker Cleanup Script
# Stops all containers and removes unused Docker resources

set -e

echo "=== Docker Cleanup Script ==="
echo ""

# Stop all running containers
echo "Stopping all running containers..."
docker stop $(docker ps -q) 2>/dev/null || echo "No running containers to stop"
echo ""

# Remove all stopped containers
echo "Removing all stopped containers..."
docker container prune -f
echo ""

# Remove all unused images
echo "Removing unused Docker images..."
docker image prune -a -f
echo ""

# Remove all unused volumes
echo "Removing unused Docker volumes..."
docker volume prune -f
echo ""

# Remove all unused networks
echo "Removing unused Docker networks..."
docker network prune -f
echo ""

# System prune (removes all unused data)
echo "Performing system-wide cleanup..."
docker system prune -a -f --volumes
echo ""

echo "=== Cleanup Complete ==="
echo ""
echo "Docker disk usage:"
docker system df
