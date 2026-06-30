#!/bin/sh
F=/root/mon/app.py
fail=0
[ -f "$F" ] && echo "STEP:app.py exists:PASS" || { echo "STEP:app.py exists:FAIL:create mon/app.py"; exit 1; }
grep -q "prometheus_client" "$F" && echo "STEP:uses prometheus_client:PASS" || { echo "STEP:uses prometheus_client:FAIL:import prometheus_client"; fail=1; }
grep -q "Counter" "$F" && echo "STEP:defines a Counter:PASS" || { echo "STEP:defines a Counter:FAIL:define a Counter metric"; fail=1; }
grep -q "start_http_server" "$F" && echo "STEP:exposes /metrics:PASS" || { echo "STEP:exposes /metrics:FAIL:call start_http_server"; fail=1; }
exit $fail
