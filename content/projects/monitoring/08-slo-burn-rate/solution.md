# Solution

```bash
mkdir -p /root/mon
cat > /root/mon/slo.rules.yml <<'YML'
groups:
  - name: slo
    rules:
      - record: job:error_ratio
        expr: rate(http_errors_total[5m]) / rate(http_requests_total[5m])
      - alert: ErrorBudgetBurn
        expr: job:error_ratio > 0.01
        for: 10m
        labels:
          severity: page
        annotations:
          summary: "Error budget burning too fast"
YML
```
