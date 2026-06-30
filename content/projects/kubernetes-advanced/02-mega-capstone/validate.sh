#!/bin/sh
P=/root/platform
fail=0
[ -f "$P/.github/workflows/ci.yml" ] && echo "STEP:CI/CD pipeline:PASS" || { echo "STEP:CI/CD pipeline:FAIL:add .github/workflows/ci.yml"; fail=1; }
ls "$P"/infra/*.tf >/dev/null 2>&1 && echo "STEP:IaC (Terraform):PASS" || { echo "STEP:IaC (Terraform):FAIL:add infra/*.tf"; fail=1; }
grep -rq "kind: Deployment" "$P/k8s" 2>/dev/null && echo "STEP:Kubernetes manifests:PASS" || { echo "STEP:Kubernetes manifests:FAIL:add a k8s Deployment"; fail=1; }
grep -rq "scrape_configs" "$P/monitoring" 2>/dev/null && echo "STEP:Monitoring config:PASS" || { echo "STEP:Monitoring config:FAIL:add monitoring/prometheus.yml"; fail=1; }
grep -rqi "trivy" "$P/security" 2>/dev/null && echo "STEP:Security scanning:PASS" || { echo "STEP:Security scanning:FAIL:add a trivy scan"; fail=1; }
exit $fail
