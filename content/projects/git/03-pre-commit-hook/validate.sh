#!/bin/sh
cd /root/repo 2>/dev/null || { echo "STEP:repo exists:FAIL:/root/repo missing"; exit 1; }
fail=0
if [ -x .git/hooks/pre-commit ]; then
  echo "STEP:pre-commit hook installed:PASS"; else echo "STEP:pre-commit hook installed:FAIL:add executable .git/hooks/pre-commit"; fail=1; fi
if git cat-file -p main:a.txt >/dev/null 2>&1; then
  echo "STEP:clean commit allowed:PASS"; else echo "STEP:clean commit allowed:FAIL:a.txt should be committed"; fail=1; fi
if ! git cat-file -p main:b.txt >/dev/null 2>&1; then
  echo "STEP:TODO commit blocked:PASS"; else echo "STEP:TODO commit blocked:FAIL:b.txt (with TODO) must be rejected by the hook"; fail=1; fi
exit $fail
