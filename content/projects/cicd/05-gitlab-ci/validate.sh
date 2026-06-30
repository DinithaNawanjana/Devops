#!/bin/sh
F=/root/repo/.gitlab-ci.yml
fail=0
[ -f "$F" ] && echo "STEP:.gitlab-ci.yml exists:PASS" || { echo "STEP:.gitlab-ci.yml exists:FAIL:create .gitlab-ci.yml"; exit 1; }
grep -q "stages:" "$F" && echo "STEP:defines stages:PASS" || { echo "STEP:defines stages:FAIL:add stages:"; fail=1; }
grep -q "cache:" "$F" && echo "STEP:uses cache:PASS" || { echo "STEP:uses cache:FAIL:add a cache:"; fail=1; }
grep -q "artifacts:" "$F" && echo "STEP:produces artifacts:PASS" || { echo "STEP:produces artifacts:FAIL:add artifacts:"; fail=1; }
exit $fail
