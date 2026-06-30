#!/bin/bash
set -e
mkdir -p /root/sec
cat > /root/sec/networkpolicy.yaml <<'YML'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
spec:
  podSelector: {}
  policyTypes:
    - Ingress
YML
