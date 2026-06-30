#!/bin/sh
fail=0
if git --git-dir=/root/remote.git rev-parse --verify feature >/dev/null 2>&1; then
  echo "STEP:feature pushed to origin:PASS"; else echo "STEP:feature pushed to origin:FAIL:push the feature branch to origin"; fail=1; fi
if git --git-dir=/root/remote.git show feature:feat.txt >/dev/null 2>&1; then
  echo "STEP:feat.txt present on remote:PASS"; else echo "STEP:feat.txt present on remote:FAIL:remote feature should contain feat.txt"; fail=1; fi
exit $fail
