#!/bin/sh
cd /root || exit 0
rm -rf dr
mkdir -p dr/data
echo alpha > dr/data/file1
echo beta  > dr/data/file2
exit 0
