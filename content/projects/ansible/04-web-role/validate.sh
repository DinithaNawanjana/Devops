#!/bin/sh
fail=0
[ -f /root/ansible/roles/web/tasks/main.yml ] && echo "STEP:role tasks/main.yml exists:PASS" || { echo "STEP:role tasks/main.yml exists:FAIL:create roles/web/tasks/main.yml"; fail=1; }
[ -f /root/ansible/site.yml ] && grep -q "roles:" /root/ansible/site.yml && echo "STEP:play applies the role:PASS" || { echo "STEP:play applies the role:FAIL:site.yml should list roles: - web"; fail=1; }
grep -q "nginx" /root/ansible/roles/web/tasks/main.yml 2>/dev/null && echo "STEP:role does real work:PASS" || { echo "STEP:role does real work:FAIL:add a task to the role"; fail=1; }
exit $fail
