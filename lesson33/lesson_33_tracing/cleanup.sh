#!/usr/bin/env bash
#
# cleanup.sh - Stop Docker containers and remove unused Docker resources
# Usage: ./cleanup.sh
#

set -e

echo "=== Docker cleanup ==="

# Stop all running containers
if command -v docker &>/dev/null; then
    RUNNING=$(docker ps -q 2>/dev/null || true)
    if [ -n "$RUNNING" ]; then
        echo "Stopping running containers..."
        docker stop $RUNNING
    else
        echo "No running containers."
    fi

    # Remove stopped containers
    echo "Removing stopped containers..."
    docker container prune -f

    # Remove unused images (dangling)
    echo "Removing dangling images..."
    docker image prune -f

    # Remove unused volumes
    echo "Removing unused volumes..."
    docker volume prune -f

    # Remove unused networks
    echo "Removing unused networks..."
    docker network prune -f

    # Optional: remove all unused images (not just dangling)
    echo "Removing unused images (all)..."
    docker image prune -a -f

    echo "=== Docker cleanup complete ==="
else
    echo "Docker not found or not in PATH. Skipping Docker cleanup."
fi
