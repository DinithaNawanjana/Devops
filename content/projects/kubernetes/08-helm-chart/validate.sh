#!/bin/sh
C=/root/k8s/mychart
fail=0
grep -q "apiVersion:" "$C/Chart.yaml" 2>/dev/null && grep -q "name:" "$C/Chart.yaml" 2>/dev/null && echo "STEP:Chart.yaml present:PASS" || { echo "STEP:Chart.yaml present:FAIL:create Chart.yaml"; fail=1; }
[ -f "$C/values.yaml" ] && echo "STEP:values.yaml present:PASS" || { echo "STEP:values.yaml present:FAIL:create values.yaml"; fail=1; }
grep -q "{{ .Values" "$C/templates/deployment.yaml" 2>/dev/null && echo "STEP:template uses .Values:PASS" || { echo "STEP:template uses .Values:FAIL:template with {{ .Values.* }}"; fail=1; }
exit $fail
