#!/usr/bin/env bash
# cleanup.sh - Stop containers and remove unused Docker resources

set -e

echo "=== Stopping all running containers ==="
docker stop $(docker ps -aq) 2>/dev/null || true

echo "=== Stopping docker-compose (if present) ==="
docker compose down 2>/dev/null || true
docker-compose down 2>/dev/null || true

echo "=== Removing stopped containers ==="
docker container prune -f

echo "=== Removing unused images ==="
docker image prune -a -f

echo "=== Removing unused volumes ==="
docker volume prune -f

echo "=== Removing unused networks ==="
docker network prune -f

echo "=== Removing build cache ==="
docker builder prune -f 2>/dev/null || true

echo "=== Docker cleanup complete ==="
