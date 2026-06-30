#!/bin/sh
F=/root/k8s/app.yaml
fail=0
d=$(grep -c "kind: Deployment" "$F" 2>/dev/null)
[ "${d:-0}" -ge 3 ] && echo "STEP:three Deployments (tiers):PASS" || { echo "STEP:three Deployments (tiers):FAIL:need frontend, backend, db"; fail=1; }
s=$(grep -c "kind: Service" "$F" 2>/dev/null)
[ "${s:-0}" -ge 3 ] && echo "STEP:a Service per tier:PASS" || { echo "STEP:a Service per tier:FAIL:add a Service for each tier"; fail=1; }
exit $fail
