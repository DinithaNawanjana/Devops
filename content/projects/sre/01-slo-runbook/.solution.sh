#!/bin/bash
set -e
mkdir -p /root/sre
cat > /root/sre/slo.yaml <<'YML'
service: checkout
objective: 99.9
window: 30d
indicator: success_rate
YML
cat > /root/sre/alerts.yaml <<'YML'
groups:
  - name: slo
    rules:
      - alert: ErrorBudgetBurn
        expr: rate(http_errors_total[5m]) / rate(http_requests_total[5m]) > 0.001
        for: 10m
YML
cat > /root/sre/runbook.md <<'MD'
# Runbook: Checkout error-budget burn

1. Check the Grafana SLO dashboard.
2. Identify the failing dependency from traces.
3. Roll back the latest deploy if correlated.
4. Page the on-call lead if budget < 0.
MD
