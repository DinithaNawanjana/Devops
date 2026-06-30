#!/bin/sh
F=/root/sec/policy.rego
fail=0
[ -f "$F" ] && echo "STEP:policy.rego exists:PASS" || { echo "STEP:policy.rego exists:FAIL:create policy.rego"; exit 1; }
grep -q "package" "$F" && echo "STEP:declares a package:PASS" || { echo "STEP:declares a package:FAIL:add a package declaration"; fail=1; }
grep -qE "deny" "$F" && echo "STEP:has a deny rule:PASS" || { echo "STEP:has a deny rule:FAIL:add a deny rule"; fail=1; }
exit $fail
