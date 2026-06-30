#!/bin/sh
F=/root/repo/.github/workflows/secure.yml
fail=0
[ -f "$F" ] && echo "STEP:secure.yml exists:PASS" || { echo "STEP:secure.yml exists:FAIL:create secure.yml"; exit 1; }
grep -q "secrets\." "$F" && echo "STEP:uses secrets context:PASS" || { echo "STEP:uses secrets context:FAIL:reference \${{ secrets.* }}"; fail=1; }
if grep -qiE "password[=:][[:space:]]*[A-Za-z0-9]{4,}" "$F"; then echo "STEP:no hardcoded credentials:FAIL:remove the literal password"; fail=1; else echo "STEP:no hardcoded credentials:PASS"; fi
exit $fail
