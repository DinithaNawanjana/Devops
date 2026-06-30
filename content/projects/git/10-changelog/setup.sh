#!/bin/sh
cd /root || exit 0
rm -rf repo
git init -q -b main repo
cd repo && git config user.email "l@d.local"; git config user.name "L"
echo a > app.txt; git add app.txt; git commit -qm "feat: add login"
echo b >> app.txt; git add app.txt; git commit -qm "fix: correct typo"
echo c >> app.txt; git add app.txt; git commit -qm "feat: add logout"
exit 0
