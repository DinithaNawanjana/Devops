#!/bin/sh
cd /root || exit 0
rm -rf inbox
mkdir -p inbox
cd inbox
for f in a.txt b.txt e.txt; do echo data > "$f"; done
echo log > c.log
echo img > d.jpg
exit 0
