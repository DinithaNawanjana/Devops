#!/bin/sh
F=/root/tf/loops.tf
fail=0
[ -f "$F" ] && echo "STEP:loops.tf exists:PASS" || { echo "STEP:loops.tf exists:FAIL:create tf/loops.tf"; exit 1; }
grep -q "count" "$F" && echo "STEP:uses count:PASS" || { echo "STEP:uses count:FAIL:use count in a resource"; fail=1; }
grep -q "for_each" "$F" && echo "STEP:uses for_each:PASS" || { echo "STEP:uses for_each:FAIL:use for_each in a resource"; fail=1; }
exit $fail
