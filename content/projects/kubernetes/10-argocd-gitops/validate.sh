#!/bin/sh
F=/root/k8s/application.yaml
fail=0
grep -q "kind: Application" "$F" 2>/dev/null && grep -q "argoproj.io" "$F" 2>/dev/null && echo "STEP:ArgoCD Application:PASS" || { echo "STEP:ArgoCD Application:FAIL:create an argoproj.io Application"; exit 1; }
grep -q "source:" "$F" && grep -q "repoURL" "$F" && echo "STEP:declares a Git source:PASS" || { echo "STEP:declares a Git source:FAIL:add source.repoURL"; fail=1; }
grep -q "destination:" "$F" && echo "STEP:declares a destination:PASS" || { echo "STEP:declares a destination:FAIL:add a destination"; fail=1; }
exit $fail
