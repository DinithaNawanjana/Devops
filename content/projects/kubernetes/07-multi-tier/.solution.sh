#!/bin/bash
set -e
mkdir -p /root/k8s
cat > /root/k8s/app.yaml <<'YML'
apiVersion: apps/v1
kind: Deployment
metadata: { name: frontend }
spec:
  replicas: 1
  selector: { matchLabels: { app: frontend } }
  template:
    metadata: { labels: { app: frontend } }
    spec: { containers: [ { name: web, image: nginx:alpine } ] }
---
apiVersion: v1
kind: Service
metadata: { name: frontend }
spec: { selector: { app: frontend }, ports: [ { port: 80 } ] }
---
apiVersion: apps/v1
kind: Deployment
metadata: { name: backend }
spec:
  replicas: 1
  selector: { matchLabels: { app: backend } }
  template:
    metadata: { labels: { app: backend } }
    spec: { containers: [ { name: api, image: nginx:alpine } ] }
---
apiVersion: v1
kind: Service
metadata: { name: backend }
spec: { selector: { app: backend }, ports: [ { port: 80 } ] }
---
apiVersion: apps/v1
kind: Deployment
metadata: { name: db }
spec:
  replicas: 1
  selector: { matchLabels: { app: db } }
  template:
    metadata: { labels: { app: db } }
    spec: { containers: [ { name: db, image: redis:7-alpine } ] }
---
apiVersion: v1
kind: Service
metadata: { name: db }
spec: { selector: { app: db }, ports: [ { port: 6379 } ] }
YML
