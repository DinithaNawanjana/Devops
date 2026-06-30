#!/bin/sh
cd /root || exit 0
rm -f status.txt missing.txt port.txt
rm -rf www
mkdir -p www
echo "<h1>Welcome to the networking lab</h1>" > www/index.html
exit 0
