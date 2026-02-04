#!/bin/bash
# Get WSL IP address for accessing services from Windows

echo "WSL Network Information:"
echo "======================"
echo ""

# Get WSL IP
WSL_IP=$(hostname -I | awk '{print $1}')
echo "WSL IP Address: $WSL_IP"
echo ""

echo "Access URLs from Windows:"
echo "  Dashboard: http://localhost:8080"
echo "  API: http://localhost:8000"
echo "  API Health: http://localhost:8000/health"
echo "  API Metrics: http://localhost:8000/metrics"
echo ""

echo "If localhost doesn't work, try:"
echo "  Dashboard: http://$WSL_IP:8080"
echo "  API: http://$WSL_IP:8000"
echo ""

echo "To check if services are running:"
echo "  bash scripts/check_services.sh"
echo ""
