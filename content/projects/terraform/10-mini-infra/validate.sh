#!/bin/sh
F=/root/tf/main.tf
fail=0
[ -f "$F" ] && echo "STEP:main.tf exists:PASS" || { echo "STEP:main.tf exists:FAIL:create tf/main.tf"; exit 1; }
n=$(grep -c '^resource ' "$F")
[ "${n:-0}" -ge 3 ] && echo "STEP:three+ resources (net/compute/storage):PASS" || { echo "STEP:three+ resources (net/compute/storage):FAIL:declare >=3 resources, found ${n:-0}"; fail=1; }
grep -q "^output " "$F" && echo "STEP:exposes an output:PASS" || { echo "STEP:exposes an output:FAIL:add an output block"; fail=1; }
exit $fail
