#!/bin/sh
F=/root/sec/.github/dependabot.yml
fail=0
[ -f "$F" ] && echo "STEP:dependabot.yml exists:PASS" || { echo "STEP:dependabot.yml exists:FAIL:create .github/dependabot.yml"; exit 1; }
grep -q "package-ecosystem" "$F" && echo "STEP:defines an ecosystem:PASS" || { echo "STEP:defines an ecosystem:FAIL:add a package-ecosystem"; fail=1; }
grep -q "schedule:" "$F" && echo "STEP:on a schedule:PASS" || { echo "STEP:on a schedule:FAIL:add a schedule"; fail=1; }
exit $fail
