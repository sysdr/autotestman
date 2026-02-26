#!/usr/bin/env bash
# Lesson 38 — Cleanup: stop containers and remove unused Docker resources.
set -e

echo "Stopping all running containers..."
docker ps -q | xargs -r docker stop 2>/dev/null || true

echo "Removing stopped containers..."
docker container prune -f

echo "Removing unused images (dangling and unused)..."
docker image prune -a -f

echo "Removing unused volumes..."
docker volume prune -f

echo "Removing unused networks..."
docker network prune -f

echo "Full system prune (optional cleanup)..."
docker system prune -f

echo "Done. Docker cleanup complete."
