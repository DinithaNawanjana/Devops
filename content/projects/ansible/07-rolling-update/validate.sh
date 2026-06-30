#!/bin/sh
F=/root/ansible/rolling.yml
fail=0
[ -f "$F" ] && echo "STEP:rolling.yml exists:PASS" || { echo "STEP:rolling.yml exists:FAIL:create ansible/rolling.yml"; exit 1; }
grep -q "serial:" "$F" && echo "STEP:batched with serial:PASS" || { echo "STEP:batched with serial:FAIL:add serial:"; fail=1; }
grep -q "handlers:" "$F" && grep -q "notify:" "$F" && echo "STEP:notify triggers a handler:PASS" || { echo "STEP:notify triggers a handler:FAIL:add a handler and notify it"; fail=1; }
exit $fail
