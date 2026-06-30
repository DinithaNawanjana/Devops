#!/bin/sh
C=/root/mon/docker-compose.yml
fail=0
grep -qi "node-exporter" "$C" 2>/dev/null && echo "STEP:node-exporter:PASS" || { echo "STEP:node-exporter:FAIL:add node-exporter"; fail=1; }
grep -qi "cadvisor" "$C" 2>/dev/null && echo "STEP:cadvisor:PASS" || { echo "STEP:cadvisor:FAIL:add cadvisor"; fail=1; }
grep -qi "prometheus" "$C" 2>/dev/null && echo "STEP:prometheus scrapes them:PASS" || { echo "STEP:prometheus scrapes them:FAIL:add prometheus"; fail=1; }
exit $fail
