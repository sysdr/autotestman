#!/usr/bin/env bash
# UQAP Lesson 76 — Build and run Dockerized tests
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

IMAGE="uqap-tests:lesson76"
REPORT_DIR="${SCRIPT_DIR}/reports"

echo "→ Building Docker image..."
docker build -t "$IMAGE" .

echo "→ Running tests..."
mkdir -p "$REPORT_DIR"
docker run --rm \
    -v "${REPORT_DIR}:/app/reports" \
    "$IMAGE"

echo "→ Verifying results..."
python3 utils/verify_result.py

echo ""
echo "→ Open report:  open reports/report.html"
