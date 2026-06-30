#!/bin/bash
set -e
cd /root/repo
git tag -a v1.0.0 -m "release 1.0.0"
echo "more" >> app.txt; git add app.txt; git commit -qm "feat: more"
git tag -a v1.1.0 -m "release 1.1.0"
