# PowerShell script to set up Windows port forwarding for WSL
# Run this script as Administrator in Windows PowerShell

Write-Host "Setting up WSL Port Forwarding..." -ForegroundColor Green
Write-Host ""

# Get WSL IP address
$wslIP = (wsl hostname -I).Trim().Split()[0]

if (-not $wslIP) {
    Write-Host "Error: Could not get WSL IP address" -ForegroundColor Red
    Write-Host "Make sure WSL is running" -ForegroundColor Yellow
    exit 1
}

Write-Host "WSL IP Address: $wslIP" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "Warning: Not running as Administrator" -ForegroundColor Yellow
    Write-Host "Port forwarding requires Administrator privileges" -ForegroundColor Yellow
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Manual commands to run:" -ForegroundColor Cyan
    Write-Host "  netsh interface portproxy add v4tov4 listenport=8000 listenaddress=0.0.0.0 connectport=8000 connectaddress=$wslIP" -ForegroundColor White
    Write-Host "  netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=8080 connectaddress=$wslIP" -ForegroundColor White
    exit 1
}

# Remove existing port forwarding (if any)
Write-Host "Removing existing port forwarding rules..." -ForegroundColor Yellow
netsh interface portproxy delete v4tov4 listenport=8000 listenaddress=0.0.0.0 2>$null
netsh interface portproxy delete v4tov4 listenport=8080 listenaddress=0.0.0.0 2>$null

# Add port forwarding
Write-Host "Adding port forwarding rules..." -ForegroundColor Yellow
netsh interface portproxy add v4tov4 listenport=8000 listenaddress=0.0.0.0 connectport=8000 connectaddress=$wslIP
netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=8080 connectaddress=$wslIP

# Show current port forwarding rules
Write-Host ""
Write-Host "Current port forwarding rules:" -ForegroundColor Green
netsh interface portproxy show all

Write-Host ""
Write-Host "Port forwarding configured successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "You can now access:" -ForegroundColor Cyan
Write-Host "  Dashboard: http://localhost:8080" -ForegroundColor White
Write-Host "  API: http://localhost:8000" -ForegroundColor White
Write-Host ""
