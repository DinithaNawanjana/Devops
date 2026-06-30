#!/bin/sh
fail=0
grep -q "kind: PersistentVolumeClaim" /root/k8s/pvc.yaml 2>/dev/null && echo "STEP:PVC manifest:PASS" || { echo "STEP:PVC manifest:FAIL:create a PersistentVolumeClaim"; fail=1; }
grep -q "volumeMounts:" /root/k8s/pod.yaml 2>/dev/null && grep -q "persistentVolumeClaim:" /root/k8s/pod.yaml 2>/dev/null && echo "STEP:pod mounts the claim:PASS" || { echo "STEP:pod mounts the claim:FAIL:mount the PVC in the pod"; fail=1; }
exit $fail
