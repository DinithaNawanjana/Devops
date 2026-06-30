#!/bin/bash
set -e
mkdir -p /root/mon
cat > /root/mon/prometheus.yml <<'YML'
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: 'app'
    static_configs:
      - targets: ['app:8080']
YML
