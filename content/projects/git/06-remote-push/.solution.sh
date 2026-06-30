#!/bin/bash
set -e
cd /root/work
git switch -qc feature
echo "feature work" > feat.txt; git add feat.txt; git commit -qm "feat: work"
git push -q origin feature
