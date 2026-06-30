#!/bin/bash
set -e
mkdir -p /root/mon
cat > /root/mon/docker-compose.yml <<'YML'
services:
  jaeger:
    image: jaegertracing/all-in-one
    ports:
      - "16686:16686"
      - "4317:4317"
YML
cat > /root/mon/otel-config.yml <<'YML'
exporters:
  otlp:
    endpoint: jaeger:4317
service:
  pipelines:
    traces:
      exporters: [otlp]
YML
