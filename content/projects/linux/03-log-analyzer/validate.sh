#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0
[ -x ./loganalyze.sh ] || { echo "STEP:loganalyze.sh exists:FAIL:create executable /root/loganalyze.sh"; exit 1; }
echo "STEP:loganalyze.sh exists:PASS"
./loganalyze.sh >/dev/null 2>&1
total=$(tr -dc '0-9' < report/total.txt 2>/dev/null)
if [ "$total" = "6" ]; then echo "STEP:total is 6:PASS"; else echo "STEP:total is 6:FAIL:got '$total'"; fail=1; fi
err=$(tr -dc '0-9' < report/error_count.txt 2>/dev/null)
if [ "$err" = "2" ]; then echo "STEP:error_count is 2:PASS"; else echo "STEP:error_count is 2:FAIL:got '$err'"; fail=1; fi
l1=$(sed -n '1p' report/top_ips.txt 2>/dev/null)
if echo "$l1" | grep -q "3" && echo "$l1" | grep -q "10.0.0.1"; then
  echo "STEP:top IP is 10.0.0.1 (3):PASS"; else echo "STEP:top IP is 10.0.0.1 (3):FAIL:top_ips.txt first line wrong"; fail=1; fi
exit $fail
