#!/bin/sh
F=/root/tf/main.tf
fail=0
[ -f "$F" ] && echo "STEP:main.tf exists:PASS" || { echo "STEP:main.tf exists:FAIL:create tf/main.tf"; exit 1; }
grep -q "terraform.workspace" "$F" && echo "STEP:uses terraform.workspace:PASS" || { echo "STEP:uses terraform.workspace:FAIL:reference terraform.workspace"; fail=1; }
exit $fail
