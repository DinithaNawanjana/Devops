#!/bin/sh
cd /root || exit 0
rm -rf lib-src lib.git app
git init -q -b main lib-src
cd lib-src && git config user.email "l@d.local"; git config user.name "L"
echo "lib v1" > lib.txt; git add lib.txt; git commit -qm "lib base"
cd /root
git clone -q --bare lib-src lib.git
git init -q -b main app
cd app && git config user.email "l@d.local"; git config user.name "L"
echo "# app" > README.md; git add README.md; git commit -qm "init"
exit 0
