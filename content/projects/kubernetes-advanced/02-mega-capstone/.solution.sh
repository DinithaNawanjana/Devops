#!/bin/bash
set -e
mkdir -p /root/platform/.github/workflows /root/platform/infra /root/platform/k8s /root/platform/monitoring /root/platform/security
echo 'name: CI
on: [push]
jobs: { build: { runs-on: ubuntu-latest, steps: [ { run: make build } ] } }' > /root/platform/.github/workflows/ci.yml
echo 'resource "docker_container" "app" { name = "app" image = "nginx:alpine" }' > /root/platform/infra/main.tf
echo 'apiVersion: apps/v1
kind: Deployment
metadata: { name: app }
spec: { replicas: 2, selector: { matchLabels: { app: app } }, template: { metadata: { labels: { app: app } }, spec: { containers: [ { name: app, image: nginx:alpine } ] } } }' > /root/platform/k8s/deployment.yaml
echo 'scrape_configs:
  - job_name: app
    static_configs:
      - targets: [app:8080]' > /root/platform/monitoring/prometheus.yml
echo 'name: Scan
on: [push]
jobs: { scan: { runs-on: ubuntu-latest, steps: [ { run: trivy image myapp:latest } ] } }' > /root/platform/security/scan.yml
