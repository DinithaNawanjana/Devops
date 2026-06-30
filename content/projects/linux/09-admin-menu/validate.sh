#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0
[ -x ./admin.sh ] || { echo "STEP:admin.sh exists:FAIL:create executable /root/admin.sh"; exit 1; }
echo "STEP:admin.sh exists:PASS"
menu=$(printf 'q\n' | ./admin.sh 2>/dev/null)
if echo "$menu" | grep -q "1)"; then echo "STEP:shows a menu:PASS"; else echo "STEP:shows a menu:FAIL:print a menu with options like 1)"; fail=1; fi
o1=$(printf '1\nq\n' | ./admin.sh 2>/dev/null)
if echo "$o1" | grep -q "System time:"; then echo "STEP:option 1 prints System time:PASS"; else echo "STEP:option 1 prints System time:FAIL:choice 1 should print 'System time:'"; fail=1; fi
o3=$(printf '3\nq\n' | ./admin.sh 2>/dev/null)
if echo "$o3" | grep -q "Hostname:"; then echo "STEP:option 3 prints Hostname:PASS"; else echo "STEP:option 3 prints Hostname:FAIL:choice 3 should print 'Hostname:'"; fail=1; fi
exit $fail
