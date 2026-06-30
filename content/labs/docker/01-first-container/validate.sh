#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0

# Step 1 — a container named 'web' is running
if docker ps --format '{{.Names}}' 2>/dev/null | grep -qx "web"; then
  echo "STEP:Container 'web' is running:PASS"
else
  echo "STEP:Container 'web' is running:FAIL:run a detached container named web"
  fail=1
fi

# Step 2 — port 8080 is published
if docker ps --filter name=web --format '{{.Ports}}' 2>/dev/null | grep -q "8080"; then
  echo "STEP:Port 8080 published:PASS"
else
  echo "STEP:Port 8080 published:FAIL:publish host 8080 to container 80 (-p 8080:80)"
  fail=1
fi

# Step 3 — Nginx responds on 8080
if curl -s -o /dev/null -w '%{http_code}' http://localhost:8080 2>/dev/null | grep -q "200"; then
  echo "STEP:Nginx responds on :8080:PASS"
else
  echo "STEP:Nginx responds on :8080:FAIL:curl http://localhost:8080 did not return 200"
  fail=1
fi

# Step 4 — marker file holds the container id
recorded=$(tr -d ' \n' < container_id.txt 2>/dev/null)
actual=$(docker ps -q --filter name=web 2>/dev/null | head -c 12)
if [ -n "$recorded" ] && [ -n "$actual" ] && echo "$recorded" | grep -q "$actual"; then
  echo "STEP:container_id.txt records the web container:PASS"
else
  echo "STEP:container_id.txt records the web container:FAIL:write the web container id to /root/container_id.txt"
  fail=1
fi

exit $fail
