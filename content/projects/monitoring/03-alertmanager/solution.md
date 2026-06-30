# Solution

```bash
mkdir -p /root/mon
cat > /root/mon/alert.rules.yml <<'YML'
groups:
  - name: app
    rules:
      - alert: HighErrorRate
        expr: rate(http_errors_total[5m]) > 0.5
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate"
YML
cat > /root/mon/alertmanager.yml <<'YML'
route:
  receiver: team
receivers:
  - name: team
    webhook_configs:
      - url: http://example/hook
YML
```
