#!/bin/sh
cd /root || exit 0
rm -rf reports data
mkdir -p data
echo a > data/one; echo b > data/two; echo c > data/three
exit 0
