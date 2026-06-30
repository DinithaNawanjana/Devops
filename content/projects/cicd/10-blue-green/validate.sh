#!/bin/sh
cd /root/deploy 2>/dev/null || { echo "STEP:deploy dir exists:FAIL:/root/deploy missing"; exit 1; }
fail=0
[ -x bluegreen.sh ] && echo "STEP:bluegreen.sh is executable:PASS" || { echo "STEP:bluegreen.sh is executable:FAIL:create executable bluegreen.sh"; exit 1; }
ln -sfn blue current
./bluegreen.sh >/dev/null 2>&1
if [ "$(readlink current)" = "green" ]; then echo "STEP:switches blue -> green:PASS"; else echo "STEP:switches blue -> green:FAIL:current should point at green"; fail=1; fi
./bluegreen.sh >/dev/null 2>&1
if [ "$(readlink current)" = "blue" ]; then echo "STEP:toggles green -> blue:PASS"; else echo "STEP:toggles green -> blue:FAIL:second run should switch back to blue"; fail=1; fi
[ -s switch.log ] && echo "STEP:logs each switch:PASS" || { echo "STEP:logs each switch:FAIL:append to switch.log"; fail=1; }
exit $fail
