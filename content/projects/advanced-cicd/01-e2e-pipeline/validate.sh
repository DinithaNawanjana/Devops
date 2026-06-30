#!/bin/sh
F=/root/pipeline/.github/workflows/e2e.yml
fail=0
[ -f "$F" ] && echo "STEP:e2e.yml exists:PASS" || { echo "STEP:e2e.yml exists:FAIL:create e2e.yml"; exit 1; }
grep -qi "trivy" "$F" && echo "STEP:scan stage:PASS" || { echo "STEP:scan stage:FAIL:add a scan stage"; fail=1; }
grep -qiE "helm|kubectl" "$F" && echo "STEP:deploy stage:PASS" || { echo "STEP:deploy stage:FAIL:add a deploy stage"; fail=1; }
c=$(grep -c "needs:" "$F"); [ "${c:-0}" -ge 3 ] && echo "STEP:stages chained build->scan->deploy->observe:PASS" || { echo "STEP:stages chained build->scan->deploy->observe:FAIL:chain 4 stages with needs"; fail=1; }
exit $fail
