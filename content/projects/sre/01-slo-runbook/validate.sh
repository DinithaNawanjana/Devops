#!/bin/sh
fail=0
grep -qi "objective" /root/sre/slo.yaml 2>/dev/null && echo "STEP:SLO with objective:PASS" || { echo "STEP:SLO with objective:FAIL:define an objective in slo.yaml"; fail=1; }
grep -q "rate(" /root/sre/alerts.yaml 2>/dev/null && grep -q "alert:" /root/sre/alerts.yaml 2>/dev/null && echo "STEP:burn-rate alert:PASS" || { echo "STEP:burn-rate alert:FAIL:add a burn-rate alert"; fail=1; }
[ -s /root/sre/runbook.md ] && echo "STEP:runbook written:PASS" || { echo "STEP:runbook written:FAIL:write runbook.md"; fail=1; }
exit $fail
