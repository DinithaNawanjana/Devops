#!/bin/sh
F=/root/ansible/deploy.yml
fail=0
[ -f "$F" ] && echo "STEP:deploy.yml exists:PASS" || { echo "STEP:deploy.yml exists:FAIL:create ansible/deploy.yml"; exit 1; }
grep -q "git:" "$F" && echo "STEP:clones the repo:PASS" || { echo "STEP:clones the repo:FAIL:use the git module"; fail=1; }
grep -q "service:" "$F" && echo "STEP:starts the service:PASS" || { echo "STEP:starts the service:FAIL:use the service module"; fail=1; }
grep -q "uri:" "$F" && echo "STEP:runs a health check:PASS" || { echo "STEP:runs a health check:FAIL:use the uri module"; fail=1; }
exit $fail
