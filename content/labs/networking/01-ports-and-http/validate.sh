#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0

# Step 1 — home page status captured as 200
if [ -f status.txt ] && grep -q "200" status.txt; then
  echo "STEP:Home page returned 200:PASS"
else
  echo "STEP:Home page returned 200:FAIL:write the status of GET / (200) to status.txt"
  fail=1
fi

# Step 2 — 404 captured for the missing path
if [ -f missing.txt ] && grep -q "404" missing.txt; then
  echo "STEP:Missing path returned 404:PASS"
else
  echo "STEP:Missing path returned 404:FAIL:write the status of /nope (404) to missing.txt"
  fail=1
fi

# Step 3 — port confirmed open
if [ -f port.txt ] && grep -qi "open" port.txt; then
  echo "STEP:Port 8000 confirmed open:PASS"
else
  echo "STEP:Port 8000 confirmed open:FAIL:use nc -z to write 'open' to port.txt"
  fail=1
fi

# Step 4 — served content exists
if [ -f www/index.html ] && grep -qi "welcome" www/index.html; then
  echo "STEP:Served index.html present:PASS"
else
  echo "STEP:Served index.html present:FAIL:/root/www/index.html should contain the welcome page"
  fail=1
fi

exit $fail
