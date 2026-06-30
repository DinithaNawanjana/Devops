#!/bin/sh
F=/root/mon/slo.rules.yml
fail=0
[ -f "$F" ] && echo "STEP:slo.rules.yml exists:PASS" || { echo "STEP:slo.rules.yml exists:FAIL:create mon/slo.rules.yml"; exit 1; }
grep -q "rate(" "$F" && echo "STEP:computes an error ratio:PASS" || { echo "STEP:computes an error ratio:FAIL:use rate() for the ratio"; fail=1; }
grep -q "alert:" "$F" && echo "STEP:alerts on burn rate:PASS" || { echo "STEP:alerts on burn rate:FAIL:add a burn-rate alert"; fail=1; }
exit $fail
