#!/bin/sh
cd /root || exit 0
rm -rf remote.git work
git init -q --bare remote.git
git init -q -b main work
cd work && git config user.email "l@d.local"; git config user.name "L"
echo base > app.txt; git add app.txt; git commit -qm "base"
git remote add origin /root/remote.git
git push -q origin main
exit 0
