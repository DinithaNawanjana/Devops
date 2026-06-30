#!/bin/bash
set -e
mkdir -p /root/chaos
cat > /root/chaos/podchaos.yaml <<'YML'
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: pod-kill
spec:
  action: pod-kill
  mode: one
  selector:
    labelSelectors:
      app: web
  duration: 30s
YML
