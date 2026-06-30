#!/bin/sh
F=/root/repo/.github/workflows/notify.yml
fail=0
[ -f "$F" ] && echo "STEP:notify.yml exists:PASS" || { echo "STEP:notify.yml exists:FAIL:create notify.yml"; exit 1; }
grep -qiE "slack|discord|webhook" "$F" && echo "STEP:has a notification step:PASS" || { echo "STEP:has a notification step:FAIL:post to Slack/Discord"; fail=1; }
grep -q "secrets\." "$F" && echo "STEP:webhook comes from a secret:PASS" || { echo "STEP:webhook comes from a secret:FAIL:use \${{ secrets.* }}"; fail=1; }
exit $fail
