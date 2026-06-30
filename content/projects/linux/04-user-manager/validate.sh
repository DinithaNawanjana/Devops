#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0
[ -x ./usermgr.sh ] || { echo "STEP:usermgr.sh exists:FAIL:create executable /root/usermgr.sh"; exit 1; }
echo "STEP:usermgr.sh exists:PASS"
: > users.db
./usermgr.sh add alice "Alice A" >/dev/null 2>&1
./usermgr.sh add bob "Bob B"   >/dev/null 2>&1
./usermgr.sh add alice "Alice A" >/dev/null 2>&1   # duplicate, must be ignored
n=$(./usermgr.sh count 2>/dev/null | tr -dc '0-9')
if [ "$n" = "2" ]; then echo "STEP:add is idempotent (count=2):PASS"; else echo "STEP:add is idempotent (count=2):FAIL:got count '$n'"; fail=1; fi
if grep -q "^alice:" users.db; then echo "STEP:alice stored:PASS"; else echo "STEP:alice stored:FAIL:alice not in users.db"; fail=1; fi
./usermgr.sh del bob >/dev/null 2>&1
if ! grep -q "^bob:" users.db; then echo "STEP:del removes bob:PASS"; else echo "STEP:del removes bob:FAIL:bob still present"; fail=1; fi
n2=$(./usermgr.sh count 2>/dev/null | tr -dc '0-9')
if [ "$n2" = "1" ]; then echo "STEP:count after delete is 1:PASS"; else echo "STEP:count after delete is 1:FAIL:got '$n2'"; fail=1; fi
exit $fail
