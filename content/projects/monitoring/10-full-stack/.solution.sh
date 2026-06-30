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
  loki:
    image: grafana/loki
    ports: ["3100:3100"]
  jaeger:
    image: jaegertracing/all-in-one
    ports: ["16686:16686"]
YML
