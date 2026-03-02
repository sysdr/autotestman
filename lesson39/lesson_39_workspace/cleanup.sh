#!/usr/bin/env bash
# Stop containers and remove unused Docker resources, containers, and images.
set -e

echo "Stopping all running containers..."
docker stop $(docker ps -q) 2>/dev/null || true

echo "Removing stopped containers..."
docker container prune -f

echo "Removing unused images..."
docker image prune -af

echo "Removing unused volumes..."
docker volume prune -f

echo "Removing unused networks..."
docker network prune -f

echo "Docker cleanup complete."
