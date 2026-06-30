#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0
DIR=/root/stack
FILE="$DIR/docker-compose.yml"

# Step 1 — compose file exists
if [ -f "$FILE" ]; then
  echo "STEP:docker-compose.yml exists:PASS"
else
  echo "STEP:docker-compose.yml exists:FAIL:create /root/stack/docker-compose.yml"
  echo "STEP:web + cache services defined:FAIL:no compose file"
  echo "STEP:Stack is up (web + cache):FAIL:no compose file"
  echo "STEP:Web responds on :8080:FAIL:no compose file"
  exit 1
fi

# Step 2 — both service images referenced
if grep -q "nginx" "$FILE" && grep -q "redis" "$FILE" \
   && grep -q "8080" "$FILE"; then
  echo "STEP:web + cache services defined:PASS"
else
  echo "STEP:web + cache services defined:FAIL:need nginx (port 8080) and redis services"
  fail=1
fi

# Bring the stack up (idempotent).
(cd "$DIR" && docker compose up -d >/dev/null 2>&1)
sleep 3

# Step 3 — two containers from this stack are running
running=$(cd "$DIR" && docker compose ps --status running --format '{{.Name}}' 2>/dev/null | grep -c .)
if [ "${running:-0}" -ge 2 ]; then
  echo "STEP:Stack is up (web + cache):PASS"
else
  echo "STEP:Stack is up (web + cache):FAIL:expected 2 running services, found ${running:-0}"
  fail=1
fi

# Step 4 — web responds
code=$(curl -s -o /dev/null -w '%{http_code}' http://localhost:8080 2>/dev/null)
if [ "$code" = "200" ]; then
  echo "STEP:Web responds on :8080:PASS"
else
  echo "STEP:Web responds on :8080:FAIL:curl http://localhost:8080 returned '$code'"
  fail=1
fi

exit $fail
