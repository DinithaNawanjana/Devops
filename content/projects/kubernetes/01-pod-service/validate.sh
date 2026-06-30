#!/bin/sh
fail=0
grep -q "kind: Pod" /root/k8s/pod.yaml 2>/dev/null && echo "STEP:Pod manifest:PASS" || { echo "STEP:Pod manifest:FAIL:create pod.yaml (kind: Pod)"; fail=1; }
grep -q "kind: Service" /root/k8s/service.yaml 2>/dev/null && echo "STEP:Service manifest:PASS" || { echo "STEP:Service manifest:FAIL:create service.yaml (kind: Service)"; fail=1; }
grep -q "selector:" /root/k8s/service.yaml 2>/dev/null && echo "STEP:Service selects the pod:PASS" || { echo "STEP:Service selects the pod:FAIL:add a selector matching the pod labels"; fail=1; }
exit $fail
