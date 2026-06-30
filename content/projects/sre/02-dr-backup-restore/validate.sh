#!/bin/sh
cd /root/dr 2>/dev/null || { echo "STEP:dr dir exists:FAIL:/root/dr missing"; exit 1; }
fail=0
[ -x backup.sh ] && [ -x restore.sh ] && echo "STEP:backup.sh + restore.sh executable:PASS" || { echo "STEP:backup.sh + restore.sh executable:FAIL:create both scripts"; exit 1; }
./backup.sh >/dev/null 2>&1
[ -f backup.tar.gz ] && echo "STEP:backup archive created:PASS" || { echo "STEP:backup archive created:FAIL:backup.sh should create backup.tar.gz"; fail=1; }
rm -rf data            # simulate disaster
./restore.sh >/dev/null 2>&1
if [ -f data/file1 ] && grep -q alpha data/file1 2>/dev/null; then echo "STEP:data restored after loss:PASS"; else echo "STEP:data restored after loss:FAIL:restore did not recover the data"; fail=1; fi
exit $fail
