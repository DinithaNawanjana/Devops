#!/bin/sh
cd /root || exit 0
rm -rf repo
git init -q -b main repo
cd repo && git config user.email "l@d.local"; git config user.name "L"
echo keep > keep.txt; git add keep.txt; git commit -qm "add keep"
echo treasure > lost.txt; git add lost.txt; git commit -qm "add lost"
git reset -q --hard HEAD~1
exit 0
