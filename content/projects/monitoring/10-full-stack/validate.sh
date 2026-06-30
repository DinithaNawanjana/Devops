#!/bin/sh
C=/root/mon/docker-compose.yml
fail=0
[ -f "$C" ] && echo "STEP:compose stack exists:PASS" || { echo "STEP:compose stack exists:FAIL:create mon/docker-compose.yml"; exit 1; }
grep -qi "prometheus" "$C" && grep -qi "grafana" "$C" && echo "STEP:metrics (prometheus + grafana):PASS" || { echo "STEP:metrics (prometheus + grafana):FAIL:add prometheus and grafana"; fail=1; }
grep -qi "loki" "$C" && echo "STEP:logs (loki):PASS" || { echo "STEP:logs (loki):FAIL:add loki"; fail=1; }
grep -qiE "jaeger|tempo" "$C" && echo "STEP:traces (jaeger/tempo):PASS" || { echo "STEP:traces (jaeger/tempo):FAIL:add a tracing backend"; fail=1; }
exit $fail
