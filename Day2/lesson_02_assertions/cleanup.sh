#!/bin/bash

# Cleanup script for Docker resources and project cleanup
# This script stops containers and removes unused Docker resources

set -e

echo "=========================================="
echo "Docker Cleanup Script"
echo "=========================================="

# Check if Docker is installed and running
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Skipping Docker cleanup."
else
    echo ""
    echo "1. Stopping all running containers..."
    docker stop $(docker ps -q) 2>/dev/null || echo "   No running containers to stop"
    
    echo ""
    echo "2. Removing all stopped containers..."
    docker rm $(docker ps -aq) 2>/dev/null || echo "   No stopped containers to remove"
    
    echo ""
    echo "3. Removing unused images..."
    docker image prune -af 2>/dev/null || echo "   No unused images to remove"
    
    echo ""
    echo "4. Removing unused volumes..."
    docker volume prune -af 2>/dev/null || echo "   No unused volumes to remove"
    
    echo ""
    echo "5. Removing unused networks..."
    docker network prune -af 2>/dev/null || echo "   No unused networks to remove"
    
    echo ""
    echo "6. Performing system prune (removes all unused data)..."
    docker system prune -af --volumes 2>/dev/null || echo "   System prune completed"
    
    echo ""
    echo "✅ Docker cleanup completed!"
fi

echo ""
echo "=========================================="
echo "Project Cleanup"
echo "=========================================="

# Remove Python cache files
echo ""
echo "7. Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
find . -type f -name "*.pyd" -delete 2>/dev/null || true
echo "   ✅ Python cache files removed"

# Remove pytest cache
echo ""
echo "8. Removing pytest cache..."
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
echo "   ✅ Pytest cache removed"

# Remove node_modules
echo ""
echo "9. Removing node_modules..."
find . -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
echo "   ✅ node_modules removed"

# Remove virtual environments
echo ""
echo "10. Removing virtual environments..."
find . -type d -name "venv" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".venv" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "env" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".env" -exec rm -rf {} + 2>/dev/null || true
echo "   ✅ Virtual environments removed"

# Remove Istio files
echo ""
echo "11. Removing Istio files..."
find . -type f -name "*istio*" -delete 2>/dev/null || true
find . -type d -name "*istio*" -exec rm -rf {} + 2>/dev/null || true
echo "   ✅ Istio files removed"

echo ""
echo "=========================================="
echo "✅ All cleanup operations completed!"
echo "=========================================="
