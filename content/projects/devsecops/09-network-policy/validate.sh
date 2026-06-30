#!/bin/sh
F=/root/sec/networkpolicy.yaml
fail=0
grep -q "kind: NetworkPolicy" "$F" 2>/dev/null && echo "STEP:NetworkPolicy manifest:PASS" || { echo "STEP:NetworkPolicy manifest:FAIL:create a NetworkPolicy"; exit 1; }
grep -q "podSelector:" "$F" && echo "STEP:has a podSelector:PASS" || { echo "STEP:has a podSelector:FAIL:add a podSelector"; fail=1; }
grep -q "policyTypes:" "$F" && echo "STEP:declares policyTypes:PASS" || { echo "STEP:declares policyTypes:FAIL:add policyTypes"; fail=1; }
exit $fail
