#!/bin/sh
cd /root/cicd 2>/dev/null || { echo "STEP:cicd dir exists:FAIL:/root/cicd missing"; exit 1; }
fail=0
[ -x build.sh ] && echo "STEP:build.sh is executable:PASS" || { echo "STEP:build.sh is executable:FAIL:create executable build.sh"; fail=1; }
grep -q "docker build" build.sh 2>/dev/null && grep -q "docker push" build.sh 2>/dev/null && echo "STEP:builds and pushes:PASS" || { echo "STEP:builds and pushes:FAIL:script must docker build and docker push"; fail=1; }
grep -qE "VERSION" build.sh 2>/dev/null && echo "STEP:version parameterized:PASS" || { echo "STEP:version parameterized:FAIL:use a VERSION variable"; fail=1; }
if grep -qiE "(--password|-p )[A-Za-z0-9]{4,}" build.sh 2>/dev/null; then echo "STEP:no hardcoded credentials:FAIL:remove the hardcoded password"; fail=1; else echo "STEP:no hardcoded credentials:PASS"; fi
if docker info >/dev/null 2>&1; then
  docker rm -f registry >/dev/null 2>&1
  docker run -d --name registry -p 5000:5000 registry:2 >/dev/null 2>&1
  sleep 2
  ( cd /root/cicd && sh build.sh >/dev/null 2>&1 )
  curl -s http://localhost:5000/v2/_catalog | grep -qi "myapp" && echo "STEP:[runtime] image pushed:PASS" || { echo "STEP:[runtime] image pushed:FAIL:myapp not in registry catalog"; fail=1; }
  docker rm -f registry >/dev/null 2>&1
fi
exit $fail
