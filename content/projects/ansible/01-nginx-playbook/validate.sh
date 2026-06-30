#!/bin/sh
F=/root/ansible/nginx.yml
fail=0
[ -f "$F" ] && echo "STEP:nginx.yml exists:PASS" || { echo "STEP:nginx.yml exists:FAIL:create ansible/nginx.yml"; exit 1; }
grep -q "hosts:" "$F" && grep -q "tasks:" "$F" && echo "STEP:targets hosts with tasks:PASS" || { echo "STEP:targets hosts with tasks:FAIL:add hosts: and tasks:"; fail=1; }
grep -q "nginx" "$F" && echo "STEP:installs nginx:PASS" || { echo "STEP:installs nginx:FAIL:install the nginx package"; fail=1; }
grep -q "service:" "$F" && echo "STEP:manages the service:PASS" || { echo "STEP:manages the service:FAIL:use the service module"; fail=1; }
exit $fail
