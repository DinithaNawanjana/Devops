#!/bin/sh
cd /root/repo 2>/dev/null || { echo "STEP:repo exists:FAIL:/root/repo missing"; exit 1; }
fail=0
if grep -q "color=purple" config.txt 2>/dev/null; then
  echo "STEP:resolved to purple:PASS"; else echo "STEP:resolved to purple:FAIL:config.txt must contain color=purple"; fail=1; fi
if ! grep -q "<<<<<<<" config.txt 2>/dev/null; then
  echo "STEP:no conflict markers left:PASS"; else echo "STEP:no conflict markers left:FAIL:remove <<<< ==== >>>> markers"; fail=1; fi
parents=$(git rev-list --parents -n1 HEAD | wc -w)
if [ "$parents" -ge 3 ]; then
  echo "STEP:merge commit recorded:PASS"; else echo "STEP:merge commit recorded:FAIL:commit the merge (HEAD should have 2 parents)"; fail=1; fi
exit $fail
