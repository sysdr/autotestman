#!/bin/bash

# Cleanup script to stop containers and remove unused Docker resources
# Also removes development files and caches

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

echo "🧹 Starting cleanup process..."
echo ""

# Stop all services
echo "🛑 Stopping services..."
if [ -f "$PROJECT_ROOT/scripts/stop_api.sh" ]; then
    bash "$PROJECT_ROOT/scripts/stop_api.sh" 2>/dev/null || true
fi
if [ -f "$PROJECT_ROOT/scripts/stop_dashboard.sh" ]; then
    bash "$PROJECT_ROOT/scripts/stop_dashboard.sh" 2>/dev/null || true
fi
echo "✓ Services stopped"
echo ""

# Stop Docker containers
echo "🐳 Stopping Docker containers..."
if command -v docker >/dev/null 2>&1; then
    # Stop all running containers
    RUNNING_CONTAINERS=$(docker ps -q)
    if [ -n "$RUNNING_CONTAINERS" ]; then
        echo "  Stopping running containers..."
        docker stop $RUNNING_CONTAINERS 2>/dev/null || true
        echo "  ✓ Containers stopped"
    else
        echo "  No running containers found"
    fi
    
    # Remove all stopped containers
    STOPPED_CONTAINERS=$(docker ps -a -q)
    if [ -n "$STOPPED_CONTAINERS" ]; then
        echo "  Removing stopped containers..."
        docker rm $STOPPED_CONTAINERS 2>/dev/null || true
        echo "  ✓ Containers removed"
    else
        echo "  No stopped containers found"
    fi
    
    # Remove unused images
    echo "  Removing unused Docker images..."
    docker image prune -af --filter "dangling=true" 2>/dev/null || true
    echo "  ✓ Unused images removed"
    
    # Remove unused volumes
    echo "  Removing unused Docker volumes..."
    docker volume prune -af 2>/dev/null || true
    echo "  ✓ Unused volumes removed"
    
    # Remove unused networks
    echo "  Removing unused Docker networks..."
    docker network prune -af 2>/dev/null || true
    echo "  ✓ Unused networks removed"
    
    # System prune (optional - removes all unused resources)
    echo "  Performing Docker system prune..."
    docker system prune -af --volumes 2>/dev/null || true
    echo "  ✓ Docker system cleanup completed"
else
    echo "  Docker not found, skipping Docker cleanup"
fi
echo ""

# Remove Python cache files
echo "🗑️  Removing Python cache files..."
find "$PROJECT_ROOT" -type d -name "__pycache__" -not -path "*/\.venv/*" -exec rm -rf {} + 2>/dev/null || true
find "$PROJECT_ROOT" -type f -name "*.pyc" -not -path "*/\.venv/*" -delete 2>/dev/null || true
find "$PROJECT_ROOT" -type f -name "*.pyo" -not -path "*/\.venv/*" -delete 2>/dev/null || true
find "$PROJECT_ROOT" -type f -name "*.pyd" -not -path "*/\.venv/*" -delete 2>/dev/null || true
find "$PROJECT_ROOT" -type d -name "*.egg-info" -not -path "*/\.venv/*" -exec rm -rf {} + 2>/dev/null || true
echo "✓ Python cache files removed"
echo ""

# Remove pytest cache
echo "🗑️  Removing pytest cache..."
find "$PROJECT_ROOT" -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
echo "✓ Pytest cache removed"
echo ""

# Remove virtual environments
echo "🗑️  Removing virtual environments..."
if [ -d "$PROJECT_ROOT/.venv" ]; then
    rm -rf "$PROJECT_ROOT/.venv"
    echo "  ✓ Removed .venv"
fi
if [ -d "$PROJECT_ROOT/venv" ]; then
    rm -rf "$PROJECT_ROOT/venv"
    echo "  ✓ Removed venv"
fi
echo "✓ Virtual environments removed"
echo ""

# Remove node_modules
echo "🗑️  Removing node_modules..."
find "$PROJECT_ROOT" -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
echo "✓ node_modules removed"
echo ""

# Remove Istio files
echo "🗑️  Removing Istio files..."
find "$PROJECT_ROOT" -type d -name "*istio*" -o -name "*Istio*" 2>/dev/null | while read dir; do
    if [ -d "$dir" ]; then
        rm -rf "$dir"
        echo "  ✓ Removed $dir"
    fi
done
find "$PROJECT_ROOT" -type f -name "*istio*" -o -name "*Istio*" 2>/dev/null | while read file; do
    if [ -f "$file" ]; then
        rm -f "$file"
        echo "  ✓ Removed $file"
    fi
done
echo "✓ Istio files removed"
echo ""

# Remove log files
echo "🗑️  Cleaning log files..."
if [ -d "$PROJECT_ROOT/logs" ]; then
    find "$PROJECT_ROOT/logs" -type f -name "*.log" -delete 2>/dev/null || true
    find "$PROJECT_ROOT/logs" -type f -name "*.pid" -delete 2>/dev/null || true
    echo "✓ Log files cleaned"
fi
echo ""

# Remove temporary files
echo "🗑️  Removing temporary files..."
find "$PROJECT_ROOT" -type f -name "*.tmp" -delete 2>/dev/null || true
find "$PROJECT_ROOT" -type f -name "*.temp" -delete 2>/dev/null || true
find "$PROJECT_ROOT" -type f -name ".DS_Store" -delete 2>/dev/null || true
find "$PROJECT_ROOT" -type f -name "Thumbs.db" -delete 2>/dev/null || true
echo "✓ Temporary files removed"
echo ""

# Summary
echo "✅ Cleanup completed!"
echo ""
echo "Summary:"
echo "  - Services stopped"
echo "  - Docker containers and resources cleaned"
echo "  - Python cache files removed"
echo "  - Virtual environments removed"
echo "  - node_modules removed"
echo "  - Istio files removed"
echo "  - Log files cleaned"
echo ""
