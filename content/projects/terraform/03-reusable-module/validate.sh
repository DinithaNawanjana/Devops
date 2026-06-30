#!/bin/sh
fail=0
[ -f /root/tf/modules/webserver/main.tf ] && echo "STEP:module directory exists:PASS" || { echo "STEP:module directory exists:FAIL:create modules/webserver/main.tf"; fail=1; }
if grep -q "^module " /root/tf/main.tf 2>/dev/null && grep -q "source" /root/tf/main.tf 2>/dev/null; then echo "STEP:root calls the module:PASS"; else echo "STEP:root calls the module:FAIL:add a module block with source"; fail=1; fi
exit $fail
