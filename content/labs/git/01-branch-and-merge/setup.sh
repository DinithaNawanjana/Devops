#!/bin/sh
cd /root || exit 0
rm -rf repo
mkdir -p repo
cd repo
git init -q
# Ensure an identity exists even if the system config is absent.
git config user.email "learner@devops.local"
git config user.name "DevOps Learner"
git symbolic-ref HEAD refs/heads/main 2>/dev/null || true
exit 0
