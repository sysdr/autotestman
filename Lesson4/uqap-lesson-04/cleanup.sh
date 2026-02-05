#!/bin/bash
#
# Cleanup script for Docker resources and project artifacts
# Stops containers, removes unused Docker resources, and cleans up project files
#

set -e

echo "=========================================="
echo "Docker & Project Cleanup Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Stop all running containers
echo "1. Stopping all running Docker containers..."
if docker ps -q | grep -q .; then
    CONTAINERS=$(docker ps -q)
    docker stop $CONTAINERS 2>/dev/null || true
    print_status "Stopped $(echo $CONTAINERS | wc -w) running container(s)"
else
    print_warning "No running containers found"
fi

# Remove all stopped containers
echo ""
echo "2. Removing stopped containers..."
if docker ps -aq | grep -q .; then
    STOPPED=$(docker ps -aq)
    docker rm $STOPPED 2>/dev/null || true
    print_status "Removed stopped containers"
else
    print_warning "No stopped containers found"
fi

# Remove unused images
echo ""
echo "3. Removing unused Docker images..."
if docker images -q | grep -q .; then
    UNUSED_IMAGES=$(docker images -f "dangling=true" -q)
    if [ -n "$UNUSED_IMAGES" ]; then
        docker rmi $UNUSED_IMAGES 2>/dev/null || true
        print_status "Removed dangling images"
    else
        print_warning "No dangling images found"
    fi
else
    print_warning "No images found"
fi

# Remove unused volumes
echo ""
echo "4. Removing unused Docker volumes..."
if docker volume ls -q | grep -q .; then
    UNUSED_VOLUMES=$(docker volume ls -f "dangling=true" -q)
    if [ -n "$UNUSED_VOLUMES" ]; then
        docker volume rm $UNUSED_VOLUMES 2>/dev/null || true
        print_status "Removed unused volumes"
    else
        print_warning "No unused volumes found"
    fi
else
    print_warning "No volumes found"
fi

# Remove unused networks (except default)
echo ""
echo "5. Removing unused Docker networks..."
if docker network ls -q | grep -q .; then
    UNUSED_NETWORKS=$(docker network ls -q --filter "type=custom")
    if [ -n "$UNUSED_NETWORKS" ]; then
        # Filter out default networks
        for net in $UNUSED_NETWORKS; do
            NET_NAME=$(docker network inspect $net --format '{{.Name}}' 2>/dev/null || echo "")
            if [ -n "$NET_NAME" ] && [ "$NET_NAME" != "bridge" ] && [ "$NET_NAME" != "host" ] && [ "$NET_NAME" != "none" ]; then
                docker network rm $net 2>/dev/null || true
            fi
        done
        print_status "Removed unused networks"
    else
        print_warning "No unused networks found"
    fi
else
    print_warning "No networks found"
fi

# Docker system prune (optional - commented out by default)
# Uncomment the following lines if you want to do a full system prune
# echo ""
# echo "6. Running Docker system prune..."
# docker system prune -af --volumes 2>/dev/null || true
# print_status "Docker system prune completed"

# Cleanup project files
echo ""
echo "6. Cleaning up project files..."
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Remove Python cache files
find "$PROJECT_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$PROJECT_DIR" -type f -name "*.pyc" -delete 2>/dev/null || true
find "$PROJECT_DIR" -type f -name "*.pyo" -delete 2>/dev/null || true
print_status "Removed Python cache files"

# Remove pytest cache
find "$PROJECT_DIR" -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
print_status "Removed pytest cache"

# Remove virtual environments (be careful with this)
if [ -d "$PROJECT_DIR/uqap-lesson-04/.venv" ]; then
    print_warning "Found .venv directory. Skipping removal (uncomment to remove)"
    # rm -rf "$PROJECT_DIR/uqap-lesson-04/.venv" 2>/dev/null || true
fi

# Remove node_modules
find "$PROJECT_DIR" -type d -name "node_modules" -exec rm -rf {} + 2>/dev/null || true
print_status "Removed node_modules directories"

# Remove Istio files
find "$PROJECT_DIR" -type f -name "*istio*" -o -name "*Istio*" 2>/dev/null | while read file; do
    rm -f "$file" 2>/dev/null || true
done
find "$PROJECT_DIR" -type d -name "*istio*" -o -name "*Istio*" 2>/dev/null | while read dir; do
    rm -rf "$dir" 2>/dev/null || true
done
print_status "Removed Istio files"

# Summary
echo ""
echo "=========================================="
echo "Cleanup Summary"
echo "=========================================="
echo "Docker containers: $(docker ps -aq | wc -l) remaining"
echo "Docker images: $(docker images -q | wc -l) remaining"
echo "Docker volumes: $(docker volume ls -q | wc -l) remaining"
echo "Docker networks: $(docker network ls -q | wc -l) remaining"
echo ""
print_status "Cleanup completed successfully!"
echo ""
