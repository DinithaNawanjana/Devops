#!/bin/sh
cd /root || exit 0
rm -rf deploy
mkdir -p deploy/blue deploy/green
echo v-blue > deploy/blue/index.html
echo v-green > deploy/green/index.html
ln -sfn blue deploy/current
exit 0
