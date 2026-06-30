#!/bin/sh
F=/root/repo/.github/workflows/deploy.yml
fail=0
[ -f "$F" ] && echo "STEP:deploy.yml exists:PASS" || { echo "STEP:deploy.yml exists:FAIL:create deploy.yml"; exit 1; }
grep -q "branches:" "$F" && grep -q "main" "$F" && echo "STEP:triggers on push to main:PASS" || { echo "STEP:triggers on push to main:FAIL:limit to branch main"; fail=1; }
grep -q "nginx/html" "$F" && echo "STEP:deploys to nginx web root:PASS" || { echo "STEP:deploys to nginx web root:FAIL:publish to /usr/share/nginx/html/"; fail=1; }
exit $fail
