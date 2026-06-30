# Solution

```bash
# Part 1 — concept answers
cat > /root/answers.txt <<'EOF'
most_control=IaaS
managed_runtime=PaaS
email_service=SaaS
survive_dc_failure=AZ
EOF

# Part 2 — cost script
cat > /root/cost.sh <<'SH'
#!/bin/bash
set -euo pipefail
rate=$(cat /root/rate.txt)
awk -v r="$rate" 'BEGIN { printf "%.2f\n", r * 730 }' > /root/monthly_cost.txt
SH
chmod 755 /root/cost.sh
/root/cost.sh
cat /root/monthly_cost.txt    # 73.00
```
