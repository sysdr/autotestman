#!/bin/bash

# Cleanup Script for Docker and Project Files
# This script stops all Docker containers and removes unused resources

set -e  # Exit on error

echo "🧹 Starting cleanup process..."

# Stop all running Docker containers
echo "📦 Stopping all Docker containers..."
docker stop $(docker ps -aq) 2>/dev/null || echo "   No running containers to stop"

# Remove all stopped containers
echo "🗑️  Removing stopped containers..."
docker rm $(docker ps -aq) 2>/dev/null || echo "   No containers to remove"

# Remove unused Docker images
echo "🖼️  Removing unused Docker images..."
docker image prune -a -f 2>/dev/null || echo "   No unused images to remove"

# Remove unused Docker volumes
echo "💾 Removing unused Docker volumes..."
docker volume prune -f 2>/dev/null || echo "   No unused volumes to remove"

# Remove unused Docker networks
echo "🌐 Removing unused Docker networks..."
docker network prune -f 2>/dev/null || echo "   No unused networks to remove"

# Remove all unused Docker resources (containers, networks, images, volumes)
echo "🧼 Performing full Docker system cleanup..."
docker system prune -a -f --volumes 2>/dev/null || echo "   Docker cleanup completed"

echo "✅ Docker cleanup completed!"

# Remove project-specific files
echo "📁 Cleaning up project files..."

# Remove Python cache files
echo "   Removing __pycache__ directories..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Remove .pyc files
echo "   Removing .pyc files..."
find . -type f -name "*.pyc" -delete 2>/dev/null || true

# Remove .pyo files
echo "   Removing .pyo files..."
find . -type f -name "*.pyo" -delete 2>/dev/null || true

# Remove pytest cache
echo "   Removing .pytest_cache directories..."
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true

# Remove node_modules (if any)
echo "   Removing node_modules directories..."
find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true

# Remove venv directories (excluding the one we might want to keep)
echo "   Removing venv directories..."
find . -type d -name "venv" -exec rm -rf {} + 2>/dev/null || true

# Remove Istio files
echo "   Removing Istio-related files..."
find . -type f -name "*istio*" -delete 2>/dev/null || true
find . -type d -name "*istio*" -exec rm -rf {} + 2>/dev/null || true

# Remove .DS_Store files (macOS)
echo "   Removing .DS_Store files..."
find . -type f -name ".DS_Store" -delete 2>/dev/null || true

# Remove temporary files
echo "   Removing temporary files..."
find . -type f -name "*.tmp" -delete 2>/dev/null || true
find . -type f -name "*.log" -delete 2>/dev/null || true

echo "✅ Project cleanup completed!"
echo ""
echo "🎉 All cleanup operations finished successfully!"
