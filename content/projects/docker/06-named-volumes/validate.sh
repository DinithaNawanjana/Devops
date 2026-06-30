#!/bin/sh
cd /root/vol 2>/dev/null || { echo "STEP:vol dir exists:FAIL:/root/vol missing"; exit 1; }
fail=0
[ -x run.sh ] && echo "STEP:run.sh is executable:PASS" || { echo "STEP:run.sh is executable:FAIL:create executable run.sh"; fail=1; }
grep -q "volume create" run.sh 2>/dev/null && echo "STEP:creates a named volume:PASS" || { echo "STEP:creates a named volume:FAIL:use docker volume create"; fail=1; }
grep -qE "\-v +labdata:" run.sh 2>/dev/null && echo "STEP:mounts the named volume:PASS" || { echo "STEP:mounts the named volume:FAIL:mount -v labdata:/data"; fail=1; }
if docker info >/dev/null 2>&1; then
  docker volume rm labdata >/dev/null 2>&1
  sh run.sh 2>/dev/null | grep -qi "persisted" && echo "STEP:[runtime] data persists across containers:PASS" || { echo "STEP:[runtime] data persists across containers:FAIL:read-back did not show persisted"; fail=1; }
  docker volume rm labdata >/dev/null 2>&1
fi
exit $fail
