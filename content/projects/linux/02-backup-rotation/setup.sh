#!/bin/sh
cd /root || exit 0
rm -rf backups
rm -rf data
mkdir -p data
echo "important config" > data/app.conf
echo "user records"     > data/users.csv
mkdir -p data/logs
echo "log line"         > data/logs/app.log
exit 0
