# Troubleshooting ERR_CONNECTION_RESET

## Issue: Cannot access dashboard from Windows browser

### Solution 1: Verify Services are Running

```bash
cd uqap-lesson-01
bash scripts/check_services.sh
```

Both API and Dashboard should show as running.

### Solution 2: Check Port Binding

Services should be bound to `0.0.0.0` (not `localhost`). Verify:

```bash
netstat -tlnp | grep -E ':(8000|8080)'
```

You should see `0.0.0.0:8000` and `0.0.0.0:8080`.

### Solution 3: Try Different URLs

**Primary (should work):**
- Dashboard: http://localhost:8080
- API: http://localhost:8000

**Alternative (if localhost doesn't work):**
- Get WSL IP: `bash get_wsl_ip.sh`
- Dashboard: http://<WSL_IP>:8080
- API: http://<WSL_IP>:8000

### Solution 4: Restart Services

If services are not accessible:

```bash
# Stop services
bash scripts/stop_api.sh
bash scripts/stop_dashboard.sh

# Wait a moment
sleep 2

# Start services
bash scripts/start_api.sh
bash scripts/start_dashboard.sh

# Verify
bash scripts/check_services.sh
```

### Solution 5: Check Windows Firewall

Windows Firewall might be blocking WSL ports. To allow:

1. Open Windows Defender Firewall
2. Click "Advanced settings"
3. Create inbound rules for ports 8000 and 8080
4. Allow TCP connections on these ports

### Solution 6: WSL Port Forwarding (if needed)

If localhost still doesn't work, you may need to set up port forwarding in Windows PowerShell (as Administrator):

```powershell
# Forward port 8000
netsh interface portproxy add v4tov4 listenport=8000 listenaddress=0.0.0.0 connectport=8000 connectaddress=<WSL_IP>

# Forward port 8080
netsh interface portproxy add v4tov4 listenport=8080 listenaddress=0.0.0.0 connectport=8080 connectaddress=<WSL_IP>
```

Replace `<WSL_IP>` with your WSL IP (run `bash get_wsl_ip.sh` to get it).

### Solution 7: Verify from WSL

Test if services are accessible from within WSL:

```bash
# Test API
curl http://localhost:8000/health

# Test Dashboard
curl http://localhost:8080
```

If these work in WSL but not from Windows, it's a port forwarding issue.

### Solution 8: Check Logs

If services fail to start, check logs:

```bash
# API logs
tail -20 logs/api.log

# Dashboard logs
tail -20 logs/dashboard.log
```

## Current Configuration

- API Host: `0.0.0.0` (accessible from all interfaces)
- API Port: `8000`
- Dashboard Host: `0.0.0.0` (accessible from all interfaces)
- Dashboard Port: `8080`

## Quick Fix Command

If nothing works, restart everything:

```bash
cd uqap-lesson-01
bash scripts/stop_api.sh
bash scripts/stop_dashboard.sh
sleep 2
bash scripts/start_api.sh
bash scripts/start_dashboard.sh
sleep 3
bash scripts/check_services.sh
```

Then try accessing http://localhost:8080 in your browser.
