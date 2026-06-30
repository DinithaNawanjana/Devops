#!/bin/sh
F=/root/tf/main.tf
fail=0
[ -f "$F" ] && echo "STEP:main.tf exists:PASS" || { echo "STEP:main.tf exists:FAIL:create tf/main.tf"; exit 1; }
grep -q "provisioner" "$F" && echo "STEP:uses a provisioner:PASS" || { echo "STEP:uses a provisioner:FAIL:add a local-exec provisioner"; fail=1; }
grep -q "ansible" "$F" && echo "STEP:hands off to Ansible:PASS" || { echo "STEP:hands off to Ansible:FAIL:run ansible-playbook from the provisioner"; fail=1; }
exit $fail
