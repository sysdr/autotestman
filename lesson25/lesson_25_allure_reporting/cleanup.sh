#!/usr/bin/env bash
# Stop containers and remove unused Docker resources (lesson25 project).

set -e

echo "Stopping all running containers..."
docker stop $(docker ps -aq) 2>/dev/null || true

echo "Removing stopped containers..."
docker container prune -f

echo "Removing unused images..."
docker image prune -a -f

echo "Removing unused volumes..."
docker volume prune -f

echo "Removing unused networks..."
docker network prune -f

echo "Docker cleanup done."
