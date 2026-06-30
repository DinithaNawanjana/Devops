#!/bin/sh
C=/root/mon/docker-compose.yml
fail=0
grep -qi "loki" "$C" 2>/dev/null && echo "STEP:loki service:PASS" || { echo "STEP:loki service:FAIL:add loki"; fail=1; }
grep -qi "promtail" "$C" 2>/dev/null && echo "STEP:promtail service:PASS" || { echo "STEP:promtail service:FAIL:add promtail"; fail=1; }
grep -qi "loki" /root/mon/promtail-config.yml 2>/dev/null && echo "STEP:promtail ships to loki:PASS" || { echo "STEP:promtail ships to loki:FAIL:point promtail at loki"; fail=1; }
exit $fail
