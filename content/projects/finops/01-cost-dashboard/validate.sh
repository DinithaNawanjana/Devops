#!/bin/sh
cd /root/finops 2>/dev/null || { echo "STEP:finops dir exists:FAIL:/root/finops missing"; exit 1; }
fail=0
[ -x cost-report.sh ] && echo "STEP:cost-report.sh executable:PASS" || { echo "STEP:cost-report.sh executable:FAIL:create cost-report.sh"; exit 1; }
./cost-report.sh >/dev/null 2>&1
t=$(tr -dc '0-9' < total.txt 2>/dev/null)
if [ "$t" = "25000" ]; then echo "STEP:total spend = 250.00:PASS"; else echo "STEP:total spend = 250.00:FAIL:total.txt should be 250.00 (got $(cat total.txt 2>/dev/null))"; fail=1; fi
if grep -qi "compute" top.txt 2>/dev/null; then echo "STEP:costliest service = compute:PASS"; else echo "STEP:costliest service = compute:FAIL:top.txt should be compute"; fail=1; fi
exit $fail
