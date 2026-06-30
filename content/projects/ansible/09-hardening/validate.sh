#!/bin/sh
F=/root/ansible/harden.yml
fail=0
[ -f "$F" ] && echo "STEP:harden.yml exists:PASS" || { echo "STEP:harden.yml exists:FAIL:create ansible/harden.yml"; exit 1; }
grep -q "PermitRootLogin" "$F" && echo "STEP:disables root SSH login:PASS" || { echo "STEP:disables root SSH login:FAIL:set PermitRootLogin no"; fail=1; }
grep -q "lineinfile:" "$F" && echo "STEP:uses an idempotent module:PASS" || { echo "STEP:uses an idempotent module:FAIL:use lineinfile for the edit"; fail=1; }
grep -qiE "ufw|firewall|iptables" "$F" && echo "STEP:enables a firewall:PASS" || { echo "STEP:enables a firewall:FAIL:enable ufw/firewall"; fail=1; }
exit $fail
