#!/bin/sh
fail=0
grep -q "^variable " /root/tf/variables.tf 2>/dev/null && echo "STEP:defines variables:PASS" || { echo "STEP:defines variables:FAIL:add a variable block in variables.tf"; fail=1; }
grep -q "^output " /root/tf/outputs.tf 2>/dev/null && echo "STEP:defines outputs:PASS" || { echo "STEP:defines outputs:FAIL:add an output block in outputs.tf"; fail=1; }
[ -f /root/tf/terraform.tfvars ] && echo "STEP:supplies a tfvars file:PASS" || { echo "STEP:supplies a tfvars file:FAIL:create terraform.tfvars"; fail=1; }
exit $fail
