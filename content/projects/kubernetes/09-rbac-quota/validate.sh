#!/bin/sh
F=/root/k8s/isolation.yaml
fail=0
grep -q "kind: Namespace" "$F" 2>/dev/null && echo "STEP:Namespace:PASS" || { echo "STEP:Namespace:FAIL:add a Namespace"; fail=1; }
grep -q "kind: Role" "$F" 2>/dev/null && grep -q "kind: RoleBinding" "$F" 2>/dev/null && echo "STEP:Role + RoleBinding:PASS" || { echo "STEP:Role + RoleBinding:FAIL:add a Role and RoleBinding"; fail=1; }
grep -q "kind: ResourceQuota" "$F" 2>/dev/null && echo "STEP:ResourceQuota:PASS" || { echo "STEP:ResourceQuota:FAIL:add a ResourceQuota"; fail=1; }
exit $fail
