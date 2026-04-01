#!/usr/bin/env bash
# Stop all containers and remove unused Docker resources (containers, images, etc.).
set -e
echo "Stopping all running containers..."
containers=$(docker ps -aq 2>/dev/null) && [[ -n "$containers" ]] && docker stop $containers || true
echo "Removing all containers..."
containers=$(docker ps -aq 2>/dev/null) && [[ -n "$containers" ]] && docker rm -f $containers || true
echo "Removing unused images..."
docker image prune -af
echo "Removing unused volumes..."
docker volume prune -f
echo "Removing unused networks..."
docker network prune -f
echo "Removing build cache..."
docker builder prune -af 2>/dev/null || true
echo "Docker cleanup complete."
