#!/usr/bin/env bash
# cleanup.sh — Stop running containers, remove unused Docker resources, then stop Docker (systemd) if available.
# Run from the workspace directory: ./cleanup.sh

set -euo pipefail

if docker info >/dev/null 2>&1; then
  echo "Stopping all running containers..."
  docker ps -q | xargs -r docker stop 2>/dev/null || true

  echo "Removing stopped containers..."
  docker container prune -f

  echo "Removing unused images (dangling and unreferenced)..."
  docker image prune -a -f

  echo "Removing build cache..."
  docker builder prune -f

  echo "Removing unused networks..."
  docker network prune -f

  echo "Removing dangling volumes..."
  docker volume prune -f
else
  echo "Docker daemon not reachable; skipping container and image cleanup."
fi

if command -v systemctl >/dev/null 2>&1; then
  if systemctl is-active --quiet docker 2>/dev/null; then
    echo "Stopping Docker service (systemd)..."
    sudo systemctl stop docker 2>/dev/null || {
      echo "Note: could not stop docker via systemctl (may need sudo or non-systemd Docker)."
    }
  fi
fi

echo "Done. Docker resources cleaned."
