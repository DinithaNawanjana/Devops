#!/bin/sh
fail=0
[ -f /root/gitops/chart/Chart.yaml ] && echo "STEP:Helm chart present:PASS" || { echo "STEP:Helm chart present:FAIL:add chart/Chart.yaml"; fail=1; }
n=$(grep -l "kind: Application" /root/gitops/app-*.yaml 2>/dev/null | wc -l)
[ "${n:-0}" -ge 2 ] && echo "STEP:two ArgoCD Applications:PASS" || { echo "STEP:two ArgoCD Applications:FAIL:add app-dev.yaml and app-prod.yaml"; fail=1; }
if grep -hq "namespace: dev" /root/gitops/app-dev.yaml 2>/dev/null && grep -hq "namespace: prod" /root/gitops/app-prod.yaml 2>/dev/null; then echo "STEP:multi-env (dev + prod):PASS"; else echo "STEP:multi-env (dev + prod):FAIL:target dev and prod namespaces"; fail=1; fi
exit $fail
