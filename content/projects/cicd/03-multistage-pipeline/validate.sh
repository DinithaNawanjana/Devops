#!/bin/sh
F=/root/repo/.github/workflows/pipeline.yml
fail=0
[ -f "$F" ] && echo "STEP:pipeline.yml exists:PASS" || { echo "STEP:pipeline.yml exists:FAIL:create pipeline.yml"; exit 1; }
if grep -qE "^  build:" "$F" && grep -qE "^  test:" "$F" && grep -qE "^  deploy:" "$F"; then echo "STEP:build/test/deploy jobs:PASS"; else echo "STEP:build/test/deploy jobs:FAIL:define build, test, deploy jobs"; fail=1; fi
n=$(grep -c "needs:" "$F")
[ "${n:-0}" -ge 2 ] && echo "STEP:jobs chained with needs:PASS" || { echo "STEP:jobs chained with needs:FAIL:use needs: to order jobs"; fail=1; }
exit $fail
