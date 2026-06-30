#!/bin/sh
cd /root/stack 2>/dev/null || { echo "STEP:stack dir exists:FAIL:/root/stack missing"; exit 1; }
F=docker-compose.yml
fail=0

# Structural checks (always run)
if [ -f "$F" ]; then echo "STEP:docker-compose.yml exists:PASS"; else echo "STEP:docker-compose.yml exists:FAIL:create /root/stack/docker-compose.yml"; exit 1; fi
if grep -q "nginx" "$F" 2>/dev/null && grep -q "redis" "$F" 2>/dev/null && grep -q "8080" "$F" 2>/dev/null; then
  echo "STEP:web + cache services defined:PASS"
else
  echo "STEP:web + cache services defined:FAIL:need nginx (port 8080) and redis services"
  fail=1
fi

# Runtime checks (only where a Docker daemon exists — always true in the lab)
if docker info >/dev/null 2>&1; then
  docker compose up -d >/dev/null 2>&1
  sleep 3
  running=$(docker compose ps --status running --format '{{.Name}}' 2>/dev/null | grep -c .)
  if [ "${running:-0}" -ge 2 ]; then echo "STEP:[runtime] stack is up (web + cache):PASS"; else echo "STEP:[runtime] stack is up (web + cache):FAIL:expected 2 running, found ${running:-0}"; fail=1; fi
  code=$(curl -s -o /dev/null -w '%{http_code}' http://localhost:8080 2>/dev/null)
  if [ "$code" = "200" ]; then echo "STEP:[runtime] web responds on :8080:PASS"; else echo "STEP:[runtime] web responds on :8080:FAIL:curl returned '$code'"; fail=1; fi
fi

exit $fail
