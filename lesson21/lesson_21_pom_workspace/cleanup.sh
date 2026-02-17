#!/usr/bin/env bash
#
# cleanup.sh - Stop Docker containers and remove unused Docker resources
# Usage: ./cleanup.sh  (run from lesson21 or project root)
#

set -e

echo "=== Docker cleanup ==="

# Stop all running containers (no-op if none)
if command -v docker &>/dev/null; then
  echo "Stopping all running containers..."
  docker stop $(docker ps -q) 2>/dev/null || true

  echo "Removing all containers (running and stopped)..."
  docker rm -f $(docker ps -aq) 2>/dev/null || true
  docker container prune -f

  echo "Removing unused images (dangling and unreferenced)..."
  docker image prune -af

  echo "Removing unused networks..."
  docker network prune -f

  echo "Removing unused volumes..."
  docker volume prune -f

  echo "Removing build cache..."
  docker builder prune -af 2>/dev/null || true

  echo "Docker cleanup complete."
  docker system df 2>/dev/null || true
else
  echo "Docker not found or not in PATH. Skipping Docker cleanup."
fi

echo "=== Cleanup finished ==="
