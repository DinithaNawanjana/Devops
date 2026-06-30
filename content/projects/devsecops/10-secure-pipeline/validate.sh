#!/bin/sh
F=/root/sec/.github/workflows/secure.yml
fail=0
[ -f "$F" ] && echo "STEP:secure.yml exists:PASS" || { echo "STEP:secure.yml exists:FAIL:create secure.yml"; exit 1; }
grep -qi "trivy" "$F" && echo "STEP:scans the image:PASS" || { echo "STEP:scans the image:FAIL:add a trivy scan"; fail=1; }
grep -qi "cosign" "$F" && echo "STEP:signs the image:PASS" || { echo "STEP:signs the image:FAIL:add a cosign sign"; fail=1; }
grep -q "needs:" "$F" && grep -qiE "deploy|kubectl" "$F" && echo "STEP:deploy gated behind scan/sign:PASS" || { echo "STEP:deploy gated behind scan/sign:FAIL:gate deploy with needs:"; fail=1; }
exit $fail
