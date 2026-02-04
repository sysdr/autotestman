#!/bin/bash
# Verify services are running and accessible

echo "=== Service Status ==="
bash scripts/check_services.sh

echo ""
echo "=== Port Binding ==="
netstat -tlnp 2>/dev/null | grep -E ':(8000|8080)' || ss -tlnp 2>/dev/null | grep -E ':(8000|8080)'

echo ""
echo "=== Service Accessibility ==="
echo -n "API Health Check: "
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✓ Accessible"
    curl -s http://localhost:8000/health
else
    echo "✗ Not accessible"
fi

echo ""
echo -n "Dashboard Check: "
if curl -s http://localhost:8080 > /dev/null 2>&1; then
    echo "✓ Accessible"
else
    echo "✗ Not accessible"
fi

echo ""
echo "=== WSL Network Info ==="
bash get_wsl_ip.sh
