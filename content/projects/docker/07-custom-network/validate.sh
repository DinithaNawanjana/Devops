#!/bin/sh
cd /root/net 2>/dev/null || { echo "STEP:net dir exists:FAIL:/root/net missing"; exit 1; }
F=docker-compose.yml
fail=0
n=$(grep -cE "^[[:space:]]+image:" "$F" 2>/dev/null)
[ "${n:-0}" -ge 3 ] && echo "STEP:three services defined:PASS" || { echo "STEP:three services defined:FAIL:need web, api, cache"; fail=1; }
grep -q "appnet" "$F" 2>/dev/null && grep -qE "^networks:" "$F" 2>/dev/null && echo "STEP:custom network appnet defined:PASS" || { echo "STEP:custom network appnet defined:FAIL:define a networks: appnet and attach services"; fail=1; }
if docker info >/dev/null 2>&1; then
  docker compose up -d >/dev/null 2>&1
  sleep 3
  r=$(docker compose ps --status running --format '{{.Name}}' 2>/dev/null | grep -c .)
  [ "${r:-0}" -ge 3 ] && echo "STEP:[runtime] 3 services running:PASS" || { echo "STEP:[runtime] 3 services running:FAIL:found ${r:-0}"; fail=1; }
  docker compose down >/dev/null 2>&1
fi
exit $fail
