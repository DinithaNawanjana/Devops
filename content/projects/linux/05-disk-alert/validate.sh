#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0
[ -x ./diskalert.sh ] || { echo "STEP:diskalert.sh exists:FAIL:create executable /root/diskalert.sh"; exit 1; }
echo "STEP:diskalert.sh exists:PASS"
: > alert.log
./diskalert.sh 0 >/dev/null 2>&1
if grep -q "ALERT" alert.txt 2>/dev/null; then echo "STEP:threshold 0 triggers ALERT:PASS"; else echo "STEP:threshold 0 triggers ALERT:FAIL:alert.txt should say ALERT"; fail=1; fi
./diskalert.sh 100 >/dev/null 2>&1
if grep -q "OK" alert.txt 2>/dev/null; then echo "STEP:threshold 100 is OK:PASS"; else echo "STEP:threshold 100 is OK:FAIL:alert.txt should say OK"; fail=1; fi
lines=$(grep -c . alert.log 2>/dev/null)
if [ "${lines:-0}" -ge 2 ]; then echo "STEP:logs every run:PASS"; else echo "STEP:logs every run:FAIL:alert.log should have a line per run"; fail=1; fi
exit $fail
