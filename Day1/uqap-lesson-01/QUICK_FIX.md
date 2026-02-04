# Quick Fix for ERR_CONNECTION_RESET

## Services are now configured to bind to 0.0.0.0

The services have been updated and restarted. Try accessing:

**Dashboard:** http://localhost:8080  
**API:** http://localhost:8000/health

## If it still doesn't work:

### Option 1: Use WSL IP Address

1. Get your WSL IP:
   ```bash
   bash get_wsl_ip.sh
   ```

2. Use the IP address shown (e.g., http://172.17.32.19:8080)

### Option 2: Set up Windows Port Forwarding

1. Open **PowerShell as Administrator** in Windows
2. Navigate to the project:
   ```powershell
   cd \\wsl.localhost\Ubuntu-24.04\home\systemdr03\git\AutoTestman\Day1\uqap-lesson-01
   ```
3. Run the port forwarding script:
   ```powershell
   .\setup_windows_port_forwarding.ps1
   ```

### Option 3: Restart Services

```bash
cd uqap-lesson-01
bash scripts/stop_api.sh
bash scripts/stop_dashboard.sh
sleep 2
bash scripts/start_api.sh
bash scripts/start_dashboard.sh
```

### Option 4: Check Windows Firewall

Windows Firewall might be blocking the ports. Temporarily disable it or add rules for ports 8000 and 8080.

## Verify Services are Running

```bash
bash scripts/check_services.sh
```

Both services should show as running.

## Test from WSL

```bash
# Should return {"status":"healthy"}
curl http://localhost:8000/health

# Should return HTML
curl http://localhost:8080
```

If these work in WSL but not from Windows, it's a port forwarding issue - use Option 2 above.
