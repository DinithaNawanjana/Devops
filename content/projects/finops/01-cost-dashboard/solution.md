# Solution

```bash
mkdir -p /root/finops
cat > /root/finops/cost-report.sh <<'SH'
#!/bin/bash
set -euo pipefail
cd /root/finops
# Total (skip header)
awk -F, 'NR>1 {sum+=$2} END {printf "%.2f\n", sum}' bill.csv > total.txt
# Costliest service (sum per service, pick max)
awk -F, 'NR>1 {s[$1]+=$2} END {for (k in s) printf "%s %.2f\n", k, s[k]}' bill.csv   | sort -k2 -rn | head -1 | awk '{print $1}' > top.txt
SH
chmod +x /root/finops/cost-report.sh
```
