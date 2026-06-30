#!/bin/sh
cd /root || exit 0
rm -rf repo
git init -q -b main repo
cd repo && git config user.email "l@d.local"; git config user.name "L"
echo v1 > app.txt; git add app.txt; git commit -qm "base"
exit 0
