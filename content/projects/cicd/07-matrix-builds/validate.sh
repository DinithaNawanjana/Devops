#!/bin/sh
F=/root/repo/.github/workflows/matrix.yml
fail=0
[ -f "$F" ] && echo "STEP:matrix.yml exists:PASS" || { echo "STEP:matrix.yml exists:FAIL:create matrix.yml"; exit 1; }
grep -q "strategy:" "$F" && grep -q "matrix:" "$F" && echo "STEP:uses a build matrix:PASS" || { echo "STEP:uses a build matrix:FAIL:add strategy: matrix:"; fail=1; }
if grep -q "3.10" "$F" && grep -q "3.12" "$F"; then echo "STEP:tests multiple versions:PASS"; else echo "STEP:tests multiple versions:FAIL:include >=3 versions"; fail=1; fi
exit $fail
