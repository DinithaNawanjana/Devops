#!/bin/sh
F=/root/repo/.github/workflows/ci.yml
fail=0
[ -f "$F" ] && echo "STEP:ci.yml exists:PASS" || { echo "STEP:ci.yml exists:FAIL:create .github/workflows/ci.yml"; exit 1; }
grep -qE "^on:|push" "$F" && echo "STEP:triggers on push:PASS" || { echo "STEP:triggers on push:FAIL:add on: push"; fail=1; }
grep -q "runs-on:" "$F" && echo "STEP:job runs-on defined:PASS" || { echo "STEP:job runs-on defined:FAIL:add runs-on"; fail=1; }
grep -q "run:" "$F" && echo "STEP:runs lint/test steps:PASS" || { echo "STEP:runs lint/test steps:FAIL:add run: steps"; fail=1; }
exit $fail
