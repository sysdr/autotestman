#!/usr/bin/env bash
# cleanup.sh — Stop containers and remove unused Docker resources.
# Run from project root: ./cleanup.sh

set -e

echo "[*] Stopping all running containers..."
docker stop $(docker ps -q) 2>/dev/null || true

echo "[*] Removing stopped containers..."
docker container prune -f

echo "[*] Removing unused images (dangling)..."
docker image prune -f

echo "[*] Removing unused networks..."
docker network prune -f

echo "[*] Removing build cache..."
docker builder prune -f

echo "[*] Optional: remove all unused images (not just dangling). Uncomment next line to run:"
# docker image prune -a -f

echo "[✓] Docker cleanup complete."
