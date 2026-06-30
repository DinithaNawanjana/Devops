# Solution

```bash
mkdir -p /root/mon
cat > /root/mon/docker-compose.yml <<'YML'
services:
  prometheus:
    image: prom/prometheus
    ports: ["9090:9090"]
  node-exporter:
    image: prom/node-exporter
    ports: ["9100:9100"]
  cadvisor:
    image: gcr.io/cadvisor/cadvisor
    ports: ["8080:8080"]
YML
```
