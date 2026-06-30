# Solution

```bash
cd /root

# 1. Total requests
wc -l < access.log > total.txt

# 2. Error count
grep -c "ERROR" access.log > errors.txt

# 3. Top 3 IPs
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -3 > top_ips.txt
```

`top_ips.txt` will look like:

```
      5 10.0.0.1
      3 10.0.0.2
      1 10.0.0.4
```
