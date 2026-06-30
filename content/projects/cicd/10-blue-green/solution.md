# Solution

```bash
cat > /root/deploy/bluegreen.sh <<'SH'
#!/bin/bash
set -euo pipefail
cd /root/deploy
current=$(readlink current)
if [ "$current" = "blue" ]; then next=green; else next=blue; fi
ln -sfn "$next" current
echo "$(date '+%F %T') switched $current -> $next" >> switch.log
SH
chmod +x /root/deploy/bluegreen.sh
```
