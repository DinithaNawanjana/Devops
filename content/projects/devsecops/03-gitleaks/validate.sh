#!/bin/sh
F=/root/sec/.github/workflows/secrets.yml
fail=0
[ -f "$F" ] && echo "STEP:secrets.yml exists:PASS" || { echo "STEP:secrets.yml exists:FAIL:create secrets.yml"; exit 1; }
grep -qi "gitleaks" "$F" && echo "STEP:runs gitleaks:PASS" || { echo "STEP:runs gitleaks:FAIL:add a gitleaks step"; fail=1; }
exit $fail
