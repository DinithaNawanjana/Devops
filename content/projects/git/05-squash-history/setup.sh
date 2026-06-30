#!/bin/sh
cd /root || exit 0
rm -rf repo
git init -q -b main repo
cd repo && git config user.email "l@d.local"; git config user.name "L"
echo "v0" > app.txt; git add app.txt; git commit -qm "base"
echo "wip1" >> app.txt; git add app.txt; git commit -qm "wip"
echo "wip2" >> app.txt; git add app.txt; git commit -qm "wip2"
echo "done" >> app.txt; git add app.txt; git commit -qm "fix typo"
exit 0
