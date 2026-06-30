#!/bin/sh
cd /root/registry 2>/dev/null || { echo "STEP:registry dir exists:FAIL:/root/registry missing"; exit 1; }
fail=0
[ -x run.sh ] && echo "STEP:run.sh is executable:PASS" || { echo "STEP:run.sh is executable:FAIL:create executable run.sh"; fail=1; }
grep -q "registry:2" run.sh 2>/dev/null && grep -q "5000" run.sh 2>/dev/null && echo "STEP:starts registry:2 on 5000:PASS" || { echo "STEP:starts registry:2 on 5000:FAIL:run registry:2 on port 5000"; fail=1; }
grep -q "push localhost:5000" run.sh 2>/dev/null && echo "STEP:pushes to localhost:5000:PASS" || { echo "STEP:pushes to localhost:5000:FAIL:docker push localhost:5000/..."; fail=1; }
if docker info >/dev/null 2>&1; then
  sh run.sh >/dev/null 2>&1
  sleep 2
  curl -s http://localhost:5000/v2/_catalog | grep -qi "demo" && echo "STEP:[runtime] image pushed to registry:PASS" || { echo "STEP:[runtime] image pushed to registry:FAIL:catalog missing demo"; fail=1; }
  docker rm -f registry >/dev/null 2>&1
fi
exit $fail
