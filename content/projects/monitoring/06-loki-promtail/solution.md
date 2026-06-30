# Solution

```bash
mkdir -p /root/mon
cat > /root/mon/docker-compose.yml <<'YML'
services:
  loki:
    image: grafana/loki
    ports: ["3100:3100"]
  promtail:
    image: grafana/promtail
    volumes:
      - ./promtail-config.yml:/etc/promtail/config.yml
YML
cat > /root/mon/promtail-config.yml <<'YML'
clients:
  - url: http://loki:3100/loki/api/v1/push
scrape_configs:
  - job_name: system
    static_configs:
      - targets: [localhost]
        labels:
          job: varlogs
          __path__: /var/log/*log
YML
```
