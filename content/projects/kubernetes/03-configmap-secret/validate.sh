#!/bin/sh
fail=0
grep -q "kind: ConfigMap" /root/k8s/config.yaml 2>/dev/null && echo "STEP:ConfigMap:PASS" || { echo "STEP:ConfigMap:FAIL:create a ConfigMap"; fail=1; }
grep -q "kind: Secret" /root/k8s/secret.yaml 2>/dev/null && echo "STEP:Secret:PASS" || { echo "STEP:Secret:FAIL:create a Secret"; fail=1; }
grep -qE "envFrom|valueFrom|configMapRef|secretRef" /root/k8s/pod.yaml 2>/dev/null && echo "STEP:injected into a pod:PASS" || { echo "STEP:injected into a pod:FAIL:inject config/secret into the pod"; fail=1; }
exit $fail
