#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0

# Step 1 — script exists and runs without error
if [ ! -f analyze.py ]; then
  echo "STEP:analyze.py runs:FAIL:/root/analyze.py missing"
  echo "STEP:total is correct:FAIL:no script"
  echo "STEP:by_status is correct:FAIL:no script"
  echo "STEP:top_path is correct:FAIL:no script"
  exit 1
fi
rm -f summary.json
if python3 analyze.py >/dev/null 2>&1 && [ -f summary.json ]; then
  echo "STEP:analyze.py runs and writes summary.json:PASS"
else
  echo "STEP:analyze.py runs and writes summary.json:FAIL:script errored or summary.json not created"
  echo "STEP:total is correct:FAIL:no output"
  echo "STEP:by_status is correct:FAIL:no output"
  echo "STEP:top_path is correct:FAIL:no output"
  exit 1
fi

# Step 2 — total == 6
total=$(jq -r '.total' summary.json 2>/dev/null)
if [ "$total" = "6" ]; then
  echo "STEP:total is correct (6):PASS"
else
  echo "STEP:total is correct (6):FAIL:expected total 6, got '$total'"
  fail=1
fi

# Step 3 — by_status counts
s200=$(jq -r '.by_status["200"]' summary.json 2>/dev/null)
s404=$(jq -r '.by_status["404"]' summary.json 2>/dev/null)
s500=$(jq -r '.by_status["500"]' summary.json 2>/dev/null)
if [ "$s200" = "4" ] && [ "$s404" = "1" ] && [ "$s500" = "1" ]; then
  echo "STEP:by_status is correct (200:4,404:1,500:1):PASS"
else
  echo "STEP:by_status is correct (200:4,404:1,500:1):FAIL:got 200=$s200 404=$s404 500=$s500"
  fail=1
fi

# Step 4 — top_path == /index
top=$(jq -r '.top_path' summary.json 2>/dev/null)
if [ "$top" = "/index" ]; then
  echo "STEP:top_path is correct (/index):PASS"
else
  echo "STEP:top_path is correct (/index):FAIL:expected /index, got '$top'"
  fail=1
fi

exit $fail
