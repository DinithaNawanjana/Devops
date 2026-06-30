#!/bin/sh
F=/root/k8s/hpa.yaml
fail=0
grep -q "kind: HorizontalPodAutoscaler" "$F" 2>/dev/null && echo "STEP:HPA manifest:PASS" || { echo "STEP:HPA manifest:FAIL:create hpa.yaml"; exit 1; }
grep -q "minReplicas:" "$F" && grep -q "maxReplicas:" "$F" && echo "STEP:min/max replicas set:PASS" || { echo "STEP:min/max replicas set:FAIL:set minReplicas and maxReplicas"; fail=1; }
grep -qi "cpu" "$F" && echo "STEP:CPU metric target:PASS" || { echo "STEP:CPU metric target:FAIL:target a CPU metric"; fail=1; }
exit $fail
