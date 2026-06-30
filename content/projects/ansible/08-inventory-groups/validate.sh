#!/bin/sh
F=/root/ansible/inventory.ini
fail=0
if [ -f "$F" ] && grep -q "\[web\]" "$F" && grep -q "\[db\]" "$F" && grep -q "\[cache\]" "$F"; then
  echo "STEP:inventory has web/db/cache groups:PASS"
else echo "STEP:inventory has web/db/cache groups:FAIL:define [web] [db] [cache]"; fail=1; fi
[ -f /root/ansible/group_vars/web.yml ] && echo "STEP:group_vars for web:PASS" || { echo "STEP:group_vars for web:FAIL:create group_vars/web.yml"; fail=1; }
exit $fail
