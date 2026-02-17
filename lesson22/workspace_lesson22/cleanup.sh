#!/bin/bash
# Cleanup Script: Stop Docker containers and remove unused Docker resources.
# Also removes project artifacts: node_modules, venv, .pytest_cache, __pycache__, .pyc, Istio.

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "$SCRIPT_DIR")"
cd "$REPO_ROOT"

echo "Stopping Docker containers and cleaning Docker resources..."

# Stop all running containers
docker stop $(docker ps -q) 2>/dev/null || true

# Stop docker compose stacks if any
docker compose down 2>/dev/null || true

# Remove stopped containers
docker container prune -f 2>/dev/null || true

# Remove unused images
docker image prune -a -f 2>/dev/null || true

# Remove unused volumes
docker volume prune -f 2>/dev/null || true

# Remove unused networks
docker network prune -f 2>/dev/null || true

# Full system prune (all unused build cache, etc.)
docker system prune -a -f --volumes 2>/dev/null || true

echo "Docker cleanup done."

# Project file cleanup (from repo root)
echo "Removing project artifacts..."

find . -type d -name "node_modules" ! -path "./.git/*" -exec rm -rf {} + 2>/dev/null || true
find . -type d \( -name "venv" -o -name ".venv" \) ! -path "./.git/*" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".pytest_cache" ! -path "./.git/*" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name "__pycache__" ! -path "./.git/*" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" ! -path "./.git/*" -delete 2>/dev/null || true
find . -type f -name "*.pyo" ! -path "./.git/*" -delete 2>/dev/null || true
find . -type f \( -name "*istio*" -o -name "*.istio.yaml" -o -name "*.istio.yml" \) ! -path "./.git/*" -delete 2>/dev/null || true
find . -type d -name "*istio*" ! -path "./.git/*" -exec rm -rf {} + 2>/dev/null || true

echo "Cleanup finished."
