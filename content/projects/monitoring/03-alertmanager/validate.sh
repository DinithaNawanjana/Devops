#!/bin/sh
fail=0
R=/root/mon/alert.rules.yml
grep -q "alert:" "$R" 2>/dev/null && grep -q "expr:" "$R" 2>/dev/null && echo "STEP:alert rule with expr:PASS" || { echo "STEP:alert rule with expr:FAIL:add an alert: with an expr:"; fail=1; }
grep -q "receivers:" /root/mon/alertmanager.yml 2>/dev/null && echo "STEP:alertmanager receivers:PASS" || { echo "STEP:alertmanager receivers:FAIL:configure receivers"; fail=1; }
exit $fail
