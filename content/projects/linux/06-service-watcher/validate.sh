#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0
[ -x ./watch.sh ] || { echo "STEP:watch.sh exists:FAIL:create executable /root/watch.sh"; exit 1; }
echo "STEP:watch.sh exists:PASS"
mkdir -p run; : > run/watch.log; rm -f run/service.up
./watch.sh >/dev/null 2>&1
if [ -f run/service.up ]; then echo "STEP:recreates missing service marker:PASS"; else echo "STEP:recreates missing service marker:FAIL:service.up not recreated"; fail=1; fi
if grep -qi "restart" run/watch.log; then echo "STEP:logs a restart event:PASS"; else echo "STEP:logs a restart event:FAIL:watch.log has no restart entry"; fail=1; fi
./watch.sh >/dev/null 2>&1
if grep -qi "ok" run/watch.log; then echo "STEP:logs ok when healthy:PASS"; else echo "STEP:logs ok when healthy:FAIL:second run should log ok"; fail=1; fi
exit $fail
