#!/bin/sh
F=/root/sec/.github/workflows/scan.yml
fail=0
[ -f "$F" ] && echo "STEP:scan.yml exists:PASS" || { echo "STEP:scan.yml exists:FAIL:create scan.yml"; exit 1; }
grep -qi "trivy" "$F" && echo "STEP:runs trivy:PASS" || { echo "STEP:runs trivy:FAIL:add a trivy scan step"; fail=1; }
grep -qiE "HIGH|CRITICAL|exit-code" "$F" && echo "STEP:fails on high severity:PASS" || { echo "STEP:fails on high severity:FAIL:gate on HIGH/CRITICAL"; fail=1; }
exit $fail
