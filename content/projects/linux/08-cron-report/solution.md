# Solution

```bash
#!/bin/bash
set -euo pipefail
mkdir -p /root/reports
n=$(find /root/data -maxdepth 1 -type f | wc -l)
echo "Files: $n" > "/root/reports/report-$(date +%F).txt"
echo "0 6 * * * /root/genreport.sh" > /root/reports/crontab.txt
```
