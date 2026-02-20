#!/bin/bash

# Cleanup Script for Docker and Project Files
# Stops all containers and removes unused Docker resources

set -e

echo "🧹 Starting cleanup process..."

# Stop all running Docker containers
echo "📦 Stopping all Docker containers..."
docker ps -q 2>/dev/null | xargs -r docker stop 2>/dev/null || echo "   No running containers to stop"

# Remove all stopped containers
echo "🗑️  Removing stopped containers..."
docker ps -aq 2>/dev/null | xargs -r docker rm 2>/dev/null || echo "   No containers to remove"

# Remove unused Docker images
echo "🖼️  Removing unused Docker images..."
docker image prune -a -f 2>/dev/null || echo "   No unused images to remove"

# Remove unused Docker volumes
echo "💾 Removing unused Docker volumes..."
docker volume prune -f 2>/dev/null || echo "   No unused volumes to remove"

# Remove unused Docker networks
echo "🌐 Removing unused Docker networks..."
docker network prune -f 2>/dev/null || echo "   No unused networks to remove"

# Full Docker system cleanup (containers, networks, images, build cache)
echo "🧼 Performing full Docker system cleanup..."
docker system prune -a -f --volumes 2>/dev/null || echo "   Docker cleanup completed"

echo "✅ Docker cleanup completed!"
echo "🎉 All cleanup operations finished successfully!"
