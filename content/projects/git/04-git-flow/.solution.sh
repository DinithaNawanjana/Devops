#!/bin/bash
set -e
cd /root/repo
git branch develop
git switch -q develop
git switch -qc feature/login
echo "login page" > login.txt; git add login.txt; git commit -qm "feat: login"
git switch -q develop
git merge --no-ff -m "merge feature/login" feature/login
