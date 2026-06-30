#!/bin/sh
F=/root/ansible/lamp.yml
fail=0
[ -f "$F" ] && echo "STEP:lamp.yml exists:PASS" || { echo "STEP:lamp.yml exists:FAIL:create ansible/lamp.yml"; exit 1; }
grep -qiE "apache2|nginx" "$F" && echo "STEP:installs a web server:PASS" || { echo "STEP:installs a web server:FAIL:install apache2 or nginx"; fail=1; }
grep -qi "mysql" "$F" && echo "STEP:installs mysql:PASS" || { echo "STEP:installs mysql:FAIL:install mysql-server"; fail=1; }
grep -qi "php" "$F" && echo "STEP:installs php:PASS" || { echo "STEP:installs php:FAIL:install php"; fail=1; }
exit $fail
