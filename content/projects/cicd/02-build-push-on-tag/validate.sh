#!/bin/sh
F=/root/repo/.github/workflows/release.yml
fail=0
[ -f "$F" ] && echo "STEP:release.yml exists:PASS" || { echo "STEP:release.yml exists:FAIL:create release.yml"; exit 1; }
grep -q "tags:" "$F" && echo "STEP:triggered on tags:PASS" || { echo "STEP:triggered on tags:FAIL:trigger on tag pushes"; fail=1; }
grep -q "docker build" "$F" && grep -q "docker push" "$F" && echo "STEP:builds and pushes image:PASS" || { echo "STEP:builds and pushes image:FAIL:docker build + push"; fail=1; }
exit $fail
