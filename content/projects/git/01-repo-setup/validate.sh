#!/bin/sh
cd /root/repo 2>/dev/null || { echo "STEP:repo exists:FAIL:/root/repo missing"; exit 1; }
fail=0
if [ -f .gitignore ] && grep -q "node_modules" .gitignore && grep -q "\*.log" .gitignore; then
  echo "STEP:.gitignore has patterns:PASS"; else echo "STEP:.gitignore has patterns:FAIL:add node_modules/ and *.log"; fail=1; fi
if git cat-file -p main:README.md >/dev/null 2>&1; then
  echo "STEP:README committed on main:PASS"; else echo "STEP:README committed on main:FAIL:commit README.md"; fail=1; fi
if git rev-parse --verify develop >/dev/null 2>&1; then
  echo "STEP:develop branch exists:PASS"; else echo "STEP:develop branch exists:FAIL:create a develop branch"; fail=1; fi
exit $fail
