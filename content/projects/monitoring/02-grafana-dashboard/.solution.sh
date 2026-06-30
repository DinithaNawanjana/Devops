#!/bin/bash
set -e
mkdir -p /root/mon
cat > /root/mon/docker-compose.yml <<'YML'
services:
  prometheus:
    image: prom/prometheus
    ports: ["9090:9090"]
  grafana:
    image: grafana/grafana
    ports: ["3000:3000"]
YML
cat > /root/mon/datasource.yml <<'YML'
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090
YML
