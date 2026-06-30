#!/bin/sh
fail=0
C=/root/mon/docker-compose.yml
grep -qi "grafana" "$C" 2>/dev/null && grep -qi "prometheus" "$C" 2>/dev/null && echo "STEP:grafana + prometheus services:PASS" || { echo "STEP:grafana + prometheus services:FAIL:run grafana and prometheus"; fail=1; }
grep -qi "type: prometheus" /root/mon/datasource.yml 2>/dev/null && echo "STEP:prometheus datasource provisioned:PASS" || { echo "STEP:prometheus datasource provisioned:FAIL:add a prometheus datasource"; fail=1; }
exit $fail
