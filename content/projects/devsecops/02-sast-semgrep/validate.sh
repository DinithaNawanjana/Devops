#!/bin/sh
F=/root/sec/.github/workflows/sast.yml
fail=0
[ -f "$F" ] && echo "STEP:sast.yml exists:PASS" || { echo "STEP:sast.yml exists:FAIL:create sast.yml"; exit 1; }
grep -qiE "semgrep|bandit" "$F" && echo "STEP:runs a SAST tool:PASS" || { echo "STEP:runs a SAST tool:FAIL:run semgrep or bandit"; fail=1; }
exit $fail
