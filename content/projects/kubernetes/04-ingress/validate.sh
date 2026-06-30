#!/bin/sh
F=/root/k8s/ingress.yaml
fail=0
grep -q "kind: Ingress" "$F" 2>/dev/null && echo "STEP:Ingress manifest:PASS" || { echo "STEP:Ingress manifest:FAIL:create ingress.yaml"; exit 1; }
n=$(grep -c "path:" "$F")
[ "${n:-0}" -ge 2 ] && echo "STEP:routes two paths:PASS" || { echo "STEP:routes two paths:FAIL:add two path rules"; fail=1; }
n2=$(grep -c "name:" "$F")
[ "${n2:-0}" -ge 2 ] && echo "STEP:to two backend services:PASS" || { echo "STEP:to two backend services:FAIL:route to two services"; fail=1; }
exit $fail
