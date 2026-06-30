#!/bin/sh
F=/root/ansible/users.yml
fail=0
[ -f "$F" ] && echo "STEP:users.yml exists:PASS" || { echo "STEP:users.yml exists:FAIL:create ansible/users.yml"; exit 1; }
grep -q "user:" "$F" && echo "STEP:creates a user:PASS" || { echo "STEP:creates a user:FAIL:use the user module"; fail=1; }
grep -q "authorized_key" "$F" && echo "STEP:installs an SSH key:PASS" || { echo "STEP:installs an SSH key:FAIL:use authorized_key"; fail=1; }
exit $fail
