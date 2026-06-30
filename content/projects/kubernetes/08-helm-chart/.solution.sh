#!/bin/bash
set -e
mkdir -p /root/k8s/mychart/templates
cat > /root/k8s/mychart/Chart.yaml <<'YML'
apiVersion: v2
name: mychart
version: 0.1.0
YML
cat > /root/k8s/mychart/values.yaml <<'YML'
replicaCount: 2
image: nginx:alpine
YML
cat > /root/k8s/mychart/templates/deployment.yaml <<'YML'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Release.Name }}-web
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels: { app: web }
  template:
    metadata:
      labels: { app: web }
    spec:
      containers:
        - name: web
          image: {{ .Values.image }}
YML
