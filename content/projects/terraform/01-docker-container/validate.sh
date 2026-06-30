#!/bin/sh
F=/root/tf/main.tf
fail=0
[ -f "$F" ] && echo "STEP:main.tf exists:PASS" || { echo "STEP:main.tf exists:FAIL:create tf/main.tf"; exit 1; }
grep -q 'provider "docker"' "$F" && echo "STEP:docker provider configured:PASS" || { echo "STEP:docker provider configured:FAIL:add provider \"docker\""; fail=1; }
grep -q 'resource "docker_container"' "$F" && echo "STEP:declares a container resource:PASS" || { echo "STEP:declares a container resource:FAIL:add a docker_container resource"; fail=1; }
exit $fail
