#!/bin/sh
cd /root/full 2>/dev/null || { echo "STEP:full dir exists:FAIL:/root/full missing"; exit 1; }
F=docker-compose.yml
fail=0
n=$(grep -cE "^[[:space:]]+image:" "$F" 2>/dev/null)
[ "${n:-0}" -ge 4 ] && echo "STEP:four services defined:PASS" || { echo "STEP:four services defined:FAIL:need frontend, backend, db, proxy"; fail=1; }
grep -qi "proxy:" "$F" 2>/dev/null && grep -q "8080" "$F" 2>/dev/null && echo "STEP:proxy publishes 8080:PASS" || { echo "STEP:proxy publishes 8080:FAIL:proxy should publish 8080"; fail=1; }
grep -qi "depends_on" "$F" 2>/dev/null && echo "STEP:depends_on ordering:PASS" || { echo "STEP:depends_on ordering:FAIL:add depends_on to the proxy"; fail=1; }
if docker info >/dev/null 2>&1; then
  docker compose up -d >/dev/null 2>&1
  sleep 3
  code=$(curl -s -o /dev/null -w '%{http_code}' http://localhost:8080 2>/dev/null)
  [ "$code" = "200" ] && echo "STEP:[runtime] proxy responds 200:PASS" || { echo "STEP:[runtime] proxy responds 200:FAIL:got '$code'"; fail=1; }
  docker compose down >/dev/null 2>&1
fi
exit $fail
