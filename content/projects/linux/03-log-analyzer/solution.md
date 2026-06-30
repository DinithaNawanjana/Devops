# Solution

```bash
#!/bin/bash
set -euo pipefail
mkdir -p /root/report
LOG=/root/logs/access.log
wc -l < "$LOG" > /root/report/total.txt
awk '$4==500' "$LOG" | wc -l > /root/report/error_count.txt
awk '{print $1}' "$LOG" | sort | uniq -c | sort -rn | head -3 > /root/report/top_ips.txt
```
