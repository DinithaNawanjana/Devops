# Solution

```bash
cat > /root/sysinfo.sh <<'SCRIPT'
#!/bin/bash
set -euo pipefail

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  echo "Usage: sysinfo.sh [--help]   Print a system info dashboard."
  exit 0
fi

print_section() { echo; echo "=== $1 ==="; }

print_section "HOSTNAME"
echo "Host: $(hostname)"
echo "Uptime: $(uptime -p 2>/dev/null || cat /proc/uptime)"

print_section "CPU"
echo "Cores: $(nproc)"
echo "Load: $(cut -d' ' -f1-3 /proc/loadavg)"

print_section "MEMORY"
free -m | awk '/Mem:/{printf "Total: %s MB  Used: %s MB  Free: %s MB\n",$2,$3,$4}'

print_section "DISK"
df -h / | awk 'NR==2{printf "Root: %s used of %s (%s)\n",$3,$2,$5}'
SCRIPT

chmod 755 /root/sysinfo.sh
/root/sysinfo.sh
```
