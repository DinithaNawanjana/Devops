# Solution

```bash
#!/bin/bash
set -euo pipefail
threshold="${1:-80}"
usage=$(df -P / | awk 'NR==2{gsub("%","",$5); print $5}')
if [ "$usage" -gt "$threshold" ]; then
  echo "ALERT: / at ${usage}% (>${threshold}%)" > /root/alert.txt
else
  echo "OK: / at ${usage}% (<=${threshold}%)" > /root/alert.txt
fi
echo "$(date '+%F %T') usage=${usage}% threshold=${threshold}%" >> /root/alert.log
```
