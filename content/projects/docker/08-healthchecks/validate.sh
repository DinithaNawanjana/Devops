#!/bin/sh
cd /root/health 2>/dev/null || { echo "STEP:health dir exists:FAIL:/root/health missing"; exit 1; }
F=docker-compose.yml
fail=0
grep -qi "healthcheck:" "$F" 2>/dev/null && grep -qi "test:" "$F" 2>/dev/null && echo "STEP:healthcheck with a test:PASS" || { echo "STEP:healthcheck with a test:FAIL:add a healthcheck: test:"; fail=1; }
grep -qiE "restart:[[:space:]]*(unless-stopped|always)" "$F" 2>/dev/null && echo "STEP:restart policy set:PASS" || { echo "STEP:restart policy set:FAIL:add restart: unless-stopped"; fail=1; }
if docker info >/dev/null 2>&1; then
  docker compose up -d >/dev/null 2>&1
  ok=0
  i=0
  while [ "$i" -lt 10 ]; do
    docker compose ps 2>/dev/null | grep -qi "healthy" && { ok=1; break; }
    i=$((i+1)); sleep 2
  done
  [ "$ok" = "1" ] && echo "STEP:[runtime] container reports healthy:PASS" || { echo "STEP:[runtime] container reports healthy:FAIL:never became healthy"; fail=1; }
  docker compose down >/dev/null 2>&1
fi
exit $fail
