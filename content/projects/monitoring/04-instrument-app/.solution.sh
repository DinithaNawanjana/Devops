#!/bin/bash
set -e
mkdir -p /root/mon
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
