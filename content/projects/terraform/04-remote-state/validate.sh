#!/bin/sh
F=/root/tf/backend.tf
fail=0
[ -f "$F" ] && echo "STEP:backend.tf exists:PASS" || { echo "STEP:backend.tf exists:FAIL:create tf/backend.tf"; exit 1; }
grep -q 'backend "' "$F" && echo "STEP:configures a backend:PASS" || { echo "STEP:configures a backend:FAIL:add a backend block"; fail=1; }
exit $fail
