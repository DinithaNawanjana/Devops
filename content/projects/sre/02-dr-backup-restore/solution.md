# Solution

```bash
mkdir -p /root/dr
cat > /root/dr/backup.sh <<'SH'
#!/bin/bash
set -euo pipefail
tar -czf /root/dr/backup.tar.gz -C /root/dr/data .
SH
cat > /root/dr/restore.sh <<'SH'
#!/bin/bash
set -euo pipefail
rm -rf /root/dr/data
mkdir -p /root/dr/data
tar -xzf /root/dr/backup.tar.gz -C /root/dr/data
SH
chmod +x /root/dr/backup.sh /root/dr/restore.sh
```
