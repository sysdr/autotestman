#!/usr/bin/env bash
# cleanup.sh - Stop containers and remove unused Docker resources

set -e

echo "=== Stopping Docker Compose (if any) ==="
docker compose down 2>/dev/null || docker-compose down 2>/dev/null || true

echo "=== Stopping all running containers ==="
docker stop $(docker ps -aq) 2>/dev/null || true

echo "=== Removing all stopped containers ==="
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
