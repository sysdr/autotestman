#!/bin/bash

# Cleanup script for Lesson 19 project
# Stops Docker containers and removes unused resources
# Removes temporary files and caches

set -e  # Exit on error

echo "=========================================="
echo "🧹 Starting Cleanup Process"
echo "=========================================="
echo ""

# Stop all Docker containers
echo "📦 Stopping all Docker containers..."
docker stop $(docker ps -aq) 2>/dev/null || echo "   No running containers found"
echo ""

# Remove all Docker containers
echo "🗑️  Removing all Docker containers..."
docker rm $(docker ps -aq) 2>/dev/null || echo "   No containers to remove"
echo ""

# Remove unused Docker images
echo "🖼️  Removing unused Docker images..."
docker image prune -a -f 2>/dev/null || echo "   No unused images to remove"
echo ""

# Remove unused Docker volumes
echo "💾 Removing unused Docker volumes..."
docker volume prune -f 2>/dev/null || echo "   No unused volumes to remove"
echo ""

# Remove unused Docker networks
echo "🌐 Removing unused Docker networks..."
docker network prune -f 2>/dev/null || echo "   No unused networks to remove"
echo ""

# Remove all unused Docker resources (containers, networks, images, build cache)
echo "🧼 Performing full Docker system prune..."
docker system prune -a -f --volumes 2>/dev/null || echo "   Docker cleanup completed"
echo ""

# Stop Docker service (optional - uncomment if needed)
# echo "🛑 Stopping Docker service..."
# sudo systemctl stop docker 2>/dev/null || echo "   Docker service not running or permission denied"
# echo ""

echo "=========================================="
echo "✅ Docker Cleanup Complete"
echo "=========================================="
echo ""
