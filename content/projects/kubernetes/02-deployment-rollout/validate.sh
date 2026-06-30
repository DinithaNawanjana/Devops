#!/bin/sh
F=/root/k8s/deployment.yaml
fail=0
grep -q "kind: Deployment" "$F" 2>/dev/null && echo "STEP:Deployment manifest:PASS" || { echo "STEP:Deployment manifest:FAIL:create deployment.yaml"; exit 1; }
grep -qE "replicas: *3" "$F" && echo "STEP:3 replicas:PASS" || { echo "STEP:3 replicas:FAIL:set replicas: 3"; fail=1; }
grep -q "RollingUpdate" "$F" && echo "STEP:rolling update strategy:PASS" || { echo "STEP:rolling update strategy:FAIL:add strategy RollingUpdate"; fail=1; }
exit $fail
