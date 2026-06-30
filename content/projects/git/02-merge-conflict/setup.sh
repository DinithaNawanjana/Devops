#!/bin/sh
cd /root || exit 0
rm -rf repo
git init -q -b main repo
cd repo && git config user.email "l@d.local"; git config user.name "L"
echo "color=blue" > config.txt; git add config.txt; git commit -qm "base"
git switch -qc feature
echo "color=green" > config.txt; git add config.txt; git commit -qm "feature: green"
git switch -q main
echo "color=red" > config.txt; git add config.txt; git commit -qm "main: red"
exit 0
