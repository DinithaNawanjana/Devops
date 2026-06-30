#!/bin/sh
cd /root/repo 2>/dev/null || { echo "STEP:repo exists:FAIL:/root/repo missing"; exit 1; }
fail=0
git rev-parse --verify develop >/dev/null 2>&1 && { echo "STEP:develop branch exists:PASS"; } || { echo "STEP:develop branch exists:FAIL:create develop"; fail=1; }
git rev-parse --verify feature/login >/dev/null 2>&1 && { echo "STEP:feature/login branch exists:PASS"; } || { echo "STEP:feature/login branch exists:FAIL:create feature/login"; fail=1; }
if git cat-file -p develop:login.txt >/dev/null 2>&1; then
  echo "STEP:login.txt merged into develop:PASS"; else echo "STEP:login.txt merged into develop:FAIL:merge feature/login into develop"; fail=1; fi
exit $fail
