#!/bin/bash
# Verify cleanup was successful

echo "=== Cleanup Verification ==="
echo ""

echo "Services Status:"
bash scripts/check_services.sh 2>&1 | grep -E "service"

echo ""
echo "Docker Containers:"
docker ps -a 2>&1 | tail -n +2 | wc -l | xargs echo "  Count:"

echo ""
echo "Project Size:"
du -sh . 2>/dev/null | awk '{print "  " $1}'

echo ""
echo "Remaining Files Check:"
if [ -d ".venv" ] || [ -d "venv" ]; then
    echo "  WARNING: Virtual environment still exists"
else
    echo "  OK: No virtual environments found"
fi

if find . -type d -name "__pycache__" -not -path "*/\.*" 2>/dev/null | grep -q .; then
    echo "  WARNING: __pycache__ directories found"
else
    echo "  OK: No __pycache__ directories found"
fi

if find . -type f -name "*.pyc" -not -path "*/\.*" 2>/dev/null | grep -q .; then
    echo "  WARNING: .pyc files found"
else
    echo "  OK: No .pyc files found"
fi

if [ -d "node_modules" ]; then
    echo "  WARNING: node_modules directory found"
else
    echo "  OK: No node_modules found"
fi

echo ""
echo "=== Verification Complete ==="
