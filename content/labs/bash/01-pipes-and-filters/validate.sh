#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0

# Step 1 — total requests == 10
total=$(tr -dc '0-9' < total.txt 2>/dev/null)
if [ "$total" = "10" ]; then
  echo "STEP:Total request count:PASS"
else
  echo "STEP:Total request count:FAIL:expected 10 in total.txt, got '$total'"
  fail=1
fi

# Step 2 — error count == 3
errors=$(tr -dc '0-9' < errors.txt 2>/dev/null)
if [ "$errors" = "3" ]; then
  echo "STEP:Error line count:PASS"
else
  echo "STEP:Error line count:FAIL:expected 3 in errors.txt, got '$errors'"
  fail=1
fi

# Step 3 — top IPs ordered correctly
line1=$(sed -n '1p' top_ips.txt 2>/dev/null)
line2=$(sed -n '2p' top_ips.txt 2>/dev/null)
line3=$(sed -n '3p' top_ips.txt 2>/dev/null)
if echo "$line1" | grep -q "5" && echo "$line1" | grep -q "10.0.0.1" \
   && echo "$line2" | grep -q "10.0.0.2" \
   && [ -n "$line3" ]; then
  echo "STEP:Top 3 IPs by frequency:PASS"
else
  echo "STEP:Top 3 IPs by frequency:FAIL:expected '5 10.0.0.1' then '3 10.0.0.2' in top_ips.txt"
  fail=1
fi

exit $fail
