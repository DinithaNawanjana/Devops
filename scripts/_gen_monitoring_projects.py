#!/usr/bin/env python3
"""Authoring helper: Monitoring & Observability project set (spec §5).
Config authoring (Prometheus/Grafana/Loki/ELK/Jaeger) graded structurally.
"""
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "content" / "projects" / "monitoring"
PROJECTS = []


def proj(**kw):
    PROJECTS.append(kw)


CLEAN = "#!/bin/sh\ncd /root || exit 0\nrm -rf mon\nmkdir -p mon\nexit 0\n"

proj(
    dir="01-prometheus-scrape", id="proj-mon-prom", title="Project: Prometheus Scrape Config",
    minutes=35, points=250, prereq="[docker-01]",
    theory="""# Project: Prometheus Scraping

Prometheus pulls metrics from targets listed under `scrape_configs`. Each
`job_name` defines what to scrape and where.
""",
    instructions="""# Project Tasks

Create `/root/mon/prometheus.yml` with a `scrape_configs` section containing a
`job_name` and `static_configs` `targets`.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/mon
cat > /root/mon/prometheus.yml <<'YML'
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: 'app'
    static_configs:
      - targets: ['app:8080']
YML
""",
    validate="""#!/bin/sh
F=/root/mon/prometheus.yml
fail=0
[ -f "$F" ] && echo "STEP:prometheus.yml exists:PASS" || { echo "STEP:prometheus.yml exists:FAIL:create mon/prometheus.yml"; exit 1; }
grep -q "scrape_configs:" "$F" && echo "STEP:has scrape_configs:PASS" || { echo "STEP:has scrape_configs:FAIL:add scrape_configs"; fail=1; }
grep -q "job_name" "$F" && grep -q "targets" "$F" && echo "STEP:defines a job with targets:PASS" || { echo "STEP:defines a job with targets:FAIL:add a job_name and targets"; fail=1; }
exit $fail
""",
)

proj(
    dir="02-grafana-dashboard", id="proj-mon-grafana", title="Project: Grafana + Prometheus",
    minutes=40, points=300, prereq="[proj-mon-prom]",
    theory="""# Project: Grafana

Grafana visualizes Prometheus data. Wire it up with a provisioned `prometheus`
datasource and run both in Compose.
""",
    instructions="""# Project Tasks

In `/root/mon/`:

1. `docker-compose.yml` running **grafana** and **prometheus**.
2. `datasource.yml` provisioning a **prometheus** datasource.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/mon
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
""",
    validate="""#!/bin/sh
fail=0
C=/root/mon/docker-compose.yml
grep -qi "grafana" "$C" 2>/dev/null && grep -qi "prometheus" "$C" 2>/dev/null && echo "STEP:grafana + prometheus services:PASS" || { echo "STEP:grafana + prometheus services:FAIL:run grafana and prometheus"; fail=1; }
grep -qi "type: prometheus" /root/mon/datasource.yml 2>/dev/null && echo "STEP:prometheus datasource provisioned:PASS" || { echo "STEP:prometheus datasource provisioned:FAIL:add a prometheus datasource"; fail=1; }
exit $fail
""",
)

proj(
    dir="03-alertmanager", id="proj-mon-alerts", title="Project: Alert Rules + Alertmanager",
    minutes=40, points=300, prereq="[proj-mon-grafana]",
    theory="""# Project: Alerting

Prometheus evaluates alerting `rules` (an `alert:` with an `expr:`) and routes
firing alerts to Alertmanager `receivers`.
""",
    instructions="""# Project Tasks

In `/root/mon/`:

1. `alert.rules.yml` — a rule group with an `alert:` and an `expr:`.
2. `alertmanager.yml` — a `route` and `receivers`.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/mon
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
""",
    validate="""#!/bin/sh
fail=0
R=/root/mon/alert.rules.yml
grep -q "alert:" "$R" 2>/dev/null && grep -q "expr:" "$R" 2>/dev/null && echo "STEP:alert rule with expr:PASS" || { echo "STEP:alert rule with expr:FAIL:add an alert: with an expr:"; fail=1; }
grep -q "receivers:" /root/mon/alertmanager.yml 2>/dev/null && echo "STEP:alertmanager receivers:PASS" || { echo "STEP:alertmanager receivers:FAIL:configure receivers"; fail=1; }
exit $fail
""",
)

proj(
    dir="04-instrument-app", id="proj-mon-instrument", title="Project: Instrument an App",
    minutes=40, points=300, prereq="[proj-mon-alerts]",
    theory="""# Project: Instrumenting Code

Expose custom metrics with the Prometheus client library — define a `Counter`,
start a metrics endpoint, and increment on work.
""",
    instructions="""# Project Tasks

Create `/root/mon/app.py` that uses **`prometheus_client`** to define a
**`Counter`** and serve metrics via **`start_http_server`**.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/mon
cat > /root/mon/app.py <<'PY'
import time
from prometheus_client import Counter, start_http_server

REQUESTS = Counter("app_requests_total", "Total requests handled")

if __name__ == "__main__":
    start_http_server(8000)
    while True:
        REQUESTS.inc()
        time.sleep(1)
PY
""",
    validate="""#!/bin/sh
F=/root/mon/app.py
fail=0
[ -f "$F" ] && echo "STEP:app.py exists:PASS" || { echo "STEP:app.py exists:FAIL:create mon/app.py"; exit 1; }
grep -q "prometheus_client" "$F" && echo "STEP:uses prometheus_client:PASS" || { echo "STEP:uses prometheus_client:FAIL:import prometheus_client"; fail=1; }
grep -q "Counter" "$F" && echo "STEP:defines a Counter:PASS" || { echo "STEP:defines a Counter:FAIL:define a Counter metric"; fail=1; }
grep -q "start_http_server" "$F" && echo "STEP:exposes /metrics:PASS" || { echo "STEP:exposes /metrics:FAIL:call start_http_server"; fail=1; }
exit $fail
""",
)

proj(
    dir="05-node-cadvisor", id="proj-mon-host", title="Project: Host Monitoring",
    minutes=40, points=300, prereq="[proj-mon-instrument]",
    theory="""# Project: Full Host Metrics

`node-exporter` exposes host metrics; `cAdvisor` exposes per-container metrics.
Prometheus scrapes both.
""",
    instructions="""# Project Tasks

Create `/root/mon/docker-compose.yml` running **node-exporter**, **cadvisor**,
and **prometheus**.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/mon
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
""",
    validate="""#!/bin/sh
C=/root/mon/docker-compose.yml
fail=0
grep -qi "node-exporter" "$C" 2>/dev/null && echo "STEP:node-exporter:PASS" || { echo "STEP:node-exporter:FAIL:add node-exporter"; fail=1; }
grep -qi "cadvisor" "$C" 2>/dev/null && echo "STEP:cadvisor:PASS" || { echo "STEP:cadvisor:FAIL:add cadvisor"; fail=1; }
grep -qi "prometheus" "$C" 2>/dev/null && echo "STEP:prometheus scrapes them:PASS" || { echo "STEP:prometheus scrapes them:FAIL:add prometheus"; fail=1; }
exit $fail
""",
)

proj(
    dir="06-loki-promtail", id="proj-mon-loki", title="Project: Loki + Promtail Logging",
    minutes=40, points=300, prereq="[proj-mon-host]",
    theory="""# Project: Centralized Logs with Loki

`promtail` ships logs to `loki`, which Grafana queries — logs alongside metrics.
""",
    instructions="""# Project Tasks

In `/root/mon/`:

1. `docker-compose.yml` running **loki** and **promtail**.
2. `promtail-config.yml` pointing at loki.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/mon
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
""",
    validate="""#!/bin/sh
C=/root/mon/docker-compose.yml
fail=0
grep -qi "loki" "$C" 2>/dev/null && echo "STEP:loki service:PASS" || { echo "STEP:loki service:FAIL:add loki"; fail=1; }
grep -qi "promtail" "$C" 2>/dev/null && echo "STEP:promtail service:PASS" || { echo "STEP:promtail service:FAIL:add promtail"; fail=1; }
grep -qi "loki" /root/mon/promtail-config.yml 2>/dev/null && echo "STEP:promtail ships to loki:PASS" || { echo "STEP:promtail ships to loki:FAIL:point promtail at loki"; fail=1; }
exit $fail
""",
)

proj(
    dir="07-elk-stack", id="proj-mon-elk", title="Project: ELK Stack",
    minutes=45, points=350, prereq="[proj-mon-loki]",
    theory="""# Project: ELK

Elasticsearch stores logs, Logstash ingests/parses them, Kibana visualizes them.
""",
    instructions="""# Project Tasks

Create `/root/mon/docker-compose.yml` running **elasticsearch**, **logstash**,
and **kibana**.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/mon
cat > /root/mon/docker-compose.yml <<'YML'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.15.0
    environment:
      - discovery.type=single-node
  logstash:
    image: docker.elastic.co/logstash/logstash:8.15.0
  kibana:
    image: docker.elastic.co/kibana/kibana:8.15.0
    ports: ["5601:5601"]
YML
""",
    validate="""#!/bin/sh
C=/root/mon/docker-compose.yml
fail=0
grep -qi "elasticsearch" "$C" 2>/dev/null && echo "STEP:elasticsearch:PASS" || { echo "STEP:elasticsearch:FAIL:add elasticsearch"; fail=1; }
grep -qi "logstash" "$C" 2>/dev/null && echo "STEP:logstash:PASS" || { echo "STEP:logstash:FAIL:add logstash"; fail=1; }
grep -qi "kibana" "$C" 2>/dev/null && echo "STEP:kibana:PASS" || { echo "STEP:kibana:FAIL:add kibana"; fail=1; }
exit $fail
""",
)

proj(
    dir="08-slo-burn-rate", id="proj-mon-slo", title="Project: SLO Burn-rate Rules",
    minutes=45, points=350, prereq="[proj-mon-elk]",
    theory="""# Project: SLOs & Error Budgets

An SLO sets a target (e.g. 99.9% success). The **error-budget burn rate** is the
ratio of failures to total — alert when it burns too fast.
""",
    instructions="""# Project Tasks

Create `/root/mon/slo.rules.yml` with a recording rule for an **error ratio**
(using `rate(...)`) and an **alert** that fires when the budget burns too fast.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/mon
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
""",
    validate="""#!/bin/sh
F=/root/mon/slo.rules.yml
fail=0
[ -f "$F" ] && echo "STEP:slo.rules.yml exists:PASS" || { echo "STEP:slo.rules.yml exists:FAIL:create mon/slo.rules.yml"; exit 1; }
grep -q "rate(" "$F" && echo "STEP:computes an error ratio:PASS" || { echo "STEP:computes an error ratio:FAIL:use rate() for the ratio"; fail=1; }
grep -q "alert:" "$F" && echo "STEP:alerts on burn rate:PASS" || { echo "STEP:alerts on burn rate:FAIL:add a burn-rate alert"; fail=1; }
exit $fail
""",
)

proj(
    dir="09-tracing-jaeger", id="proj-mon-tracing", title="Project: Distributed Tracing",
    minutes=45, points=350, prereq="[proj-mon-slo]",
    theory="""# Project: Tracing

Distributed tracing follows a request across services. Run a Jaeger/OTel
collector and point apps at it via OpenTelemetry.
""",
    instructions="""# Project Tasks

In `/root/mon/`:

1. `docker-compose.yml` running **jaeger** (or an otel-collector).
2. `otel-config.yml` (or env) wiring an app to export traces.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/mon
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
""",
    validate="""#!/bin/sh
fail=0
grep -qiE "jaeger|otel" /root/mon/docker-compose.yml 2>/dev/null && echo "STEP:tracing backend running:PASS" || { echo "STEP:tracing backend running:FAIL:run jaeger or an otel collector"; fail=1; }
grep -qiE "otlp|otel|jaeger" /root/mon/otel-config.yml 2>/dev/null && echo "STEP:traces exported:PASS" || { echo "STEP:traces exported:FAIL:export traces to the backend"; fail=1; }
exit $fail
""",
)

proj(
    dir="10-full-stack", id="proj-mon-fullstack", title="Project: Full Observability Stack",
    minutes=60, points=450, prereq="[proj-mon-tracing]",
    theory="""# Project: Metrics + Logs + Traces

The three pillars in one stack: Prometheus (metrics), Loki (logs), and
Jaeger/Tempo (traces), all visualized in Grafana.
""",
    instructions="""# Project Tasks

Create `/root/mon/docker-compose.yml` running **prometheus**, **grafana**,
**loki**, and a tracing backend (**jaeger** or **tempo**) — metrics, logs, and
traces together.

Click **Check**.
""",
    setup=CLEAN,
    solution="""mkdir -p /root/mon
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
""",
    validate="""#!/bin/sh
C=/root/mon/docker-compose.yml
fail=0
[ -f "$C" ] && echo "STEP:compose stack exists:PASS" || { echo "STEP:compose stack exists:FAIL:create mon/docker-compose.yml"; exit 1; }
grep -qi "prometheus" "$C" && grep -qi "grafana" "$C" && echo "STEP:metrics (prometheus + grafana):PASS" || { echo "STEP:metrics (prometheus + grafana):FAIL:add prometheus and grafana"; fail=1; }
grep -qi "loki" "$C" && echo "STEP:logs (loki):PASS" || { echo "STEP:logs (loki):FAIL:add loki"; fail=1; }
grep -qiE "jaeger|tempo" "$C" && echo "STEP:traces (jaeger/tempo):PASS" || { echo "STEP:traces (jaeger/tempo):FAIL:add a tracing backend"; fail=1; }
exit $fail
""",
)


def write_exec(path: Path, content: str):
    path.write_text(content, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def main():
    for p in PROJECTS:
        d = BASE / p["dir"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "project.yaml").write_text(
            f"id: {p['id']}\ntitle: \"{p['title']}\"\ntrack: monitoring\n"
            f"level: advanced\nestimated_minutes: {p['minutes']}\n"
            f"image: lab-docker:latest\nprerequisites: {p['prereq']}\n"
            f"points: {p['points']}\n",
            encoding="utf-8",
        )
        (d / "theory.md").write_text(p["theory"], encoding="utf-8")
        (d / "instructions.md").write_text(p["instructions"], encoding="utf-8")
        write_exec(d / "setup.sh", p["setup"])
        write_exec(d / "validate.sh", p["validate"])
        (d / "solution.md").write_text(
            "# Solution\n\n```bash\n" + p["solution"].strip() + "\n```\n", encoding="utf-8"
        )
        write_exec(d / ".solution.sh", "#!/bin/bash\nset -e\n" + p["solution"])
    print(f"Wrote {len(PROJECTS)} monitoring projects to {BASE}")


if __name__ == "__main__":
    main()
