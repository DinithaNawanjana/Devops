#!/bin/sh
cd /root/repo 2>/dev/null || { echo "STEP:repo exists:FAIL:/root/repo missing"; exit 1; }
fail=0
if [ -f lost.txt ] && grep -q "treasure" lost.txt; then echo "STEP:lost.txt recovered:PASS"; else echo "STEP:lost.txt recovered:FAIL:restore lost.txt (treasure)"; fail=1; fi
if git cat-file -p main:lost.txt 2>/dev/null | grep -q "treasure"; then echo "STEP:recovery committed on main:PASS"; else echo "STEP:recovery committed on main:FAIL:commit the recovered lost.txt"; fail=1; fi
exit $fail
