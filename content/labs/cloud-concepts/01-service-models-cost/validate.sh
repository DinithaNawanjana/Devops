#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0

# helper: case-insensitive value lookup from answers.txt
val() { grep -i "^$1=" answers.txt 2>/dev/null | head -1 | cut -d= -f2 | tr -d ' \r' | tr 'A-Z' 'a-z'; }

# Step 1 — concept answers
if [ -f answers.txt ]; then
  ok=1
  [ "$(val most_control)" = "iaas" ] || ok=0
  [ "$(val managed_runtime)" = "paas" ] || ok=0
  [ "$(val email_service)" = "saas" ] || ok=0
  [ "$(val survive_dc_failure)" = "az" ] || ok=0
  if [ "$ok" = "1" ]; then
    echo "STEP:Concept answers correct:PASS"
  else
    echo "STEP:Concept answers correct:FAIL:check IaaS/PaaS/SaaS/AZ answers in answers.txt"
    fail=1
  fi
else
  echo "STEP:Concept answers correct:FAIL:create /root/answers.txt"
  fail=1
fi

# Step 2 — cost.sh exists and is executable
if [ -x cost.sh ]; then
  echo "STEP:cost.sh is executable:PASS"
else
  echo "STEP:cost.sh is executable:FAIL:create executable /root/cost.sh"
  fail=1
fi

# Step 3 — monthly cost computed (0.10 * 730 = 73)
rm -f monthly_cost.txt
[ -x cost.sh ] && ./cost.sh >/dev/null 2>&1
got=$(tr -d ' \r\n' < monthly_cost.txt 2>/dev/null)
case "$got" in
  73|73.0|73.00) echo "STEP:Monthly cost = 73:PASS" ;;
  *) echo "STEP:Monthly cost = 73:FAIL:expected 73 (0.10 x 730), got '$got'"; fail=1 ;;
esac

exit $fail
