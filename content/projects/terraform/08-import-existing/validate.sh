#!/bin/sh
fail=0
grep -q 'resource "docker_container"' /root/tf/main.tf 2>/dev/null && echo "STEP:resource block defined:PASS" || { echo "STEP:resource block defined:FAIL:declare the resource to import into"; fail=1; }
grep -q "terraform import" /root/tf/import.sh 2>/dev/null && echo "STEP:runs terraform import:PASS" || { echo "STEP:runs terraform import:FAIL:import.sh should call terraform import"; fail=1; }
exit $fail
