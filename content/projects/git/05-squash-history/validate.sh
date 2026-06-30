#!/bin/sh
cd /root/repo 2>/dev/null || { echo "STEP:repo exists:FAIL:/root/repo missing"; exit 1; }
fail=0
n=$(git rev-list --count main)
if [ "$n" = "2" ]; then echo "STEP:history squashed to 2 commits:PASS"; else echo "STEP:history squashed to 2 commits:FAIL:main has $n commits, expected 2"; fail=1; fi
subj=$(git log -1 --pretty=%s main)
if [ "$subj" = "feat: add feature" ]; then echo "STEP:squashed commit message correct:PASS"; else echo "STEP:squashed commit message correct:FAIL:HEAD subject is '$subj'"; fail=1; fi
if git cat-file -p main:app.txt 2>/dev/null | grep -q "done"; then echo "STEP:file content preserved:PASS"; else echo "STEP:file content preserved:FAIL:app.txt should still contain 'done'"; fail=1; fi
exit $fail
