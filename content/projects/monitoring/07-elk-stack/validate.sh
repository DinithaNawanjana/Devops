#!/bin/sh
C=/root/mon/docker-compose.yml
fail=0
grep -qi "elasticsearch" "$C" 2>/dev/null && echo "STEP:elasticsearch:PASS" || { echo "STEP:elasticsearch:FAIL:add elasticsearch"; fail=1; }
grep -qi "logstash" "$C" 2>/dev/null && echo "STEP:logstash:PASS" || { echo "STEP:logstash:FAIL:add logstash"; fail=1; }
grep -qi "kibana" "$C" 2>/dev/null && echo "STEP:kibana:PASS" || { echo "STEP:kibana:FAIL:add kibana"; fail=1; }
exit $fail
