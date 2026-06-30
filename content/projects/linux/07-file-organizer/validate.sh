#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0
[ -x ./organize.sh ] || { echo "STEP:organize.sh exists:FAIL:create executable /root/organize.sh"; exit 1; }
echo "STEP:organize.sh exists:PASS"
./organize.sh >/dev/null 2>&1
txt=$(ls inbox/txt 2>/dev/null | grep -c .)
if [ "${txt:-0}" = "3" ]; then echo "STEP:txt files grouped (3):PASS"; else echo "STEP:txt files grouped (3):FAIL:inbox/txt should hold 3 files, found ${txt:-0}"; fail=1; fi
if [ -f inbox/log/c.log ]; then echo "STEP:log file grouped:PASS"; else echo "STEP:log file grouped:FAIL:inbox/log/c.log missing"; fail=1; fi
if [ -f inbox/jpg/d.jpg ]; then echo "STEP:jpg file grouped:PASS"; else echo "STEP:jpg file grouped:FAIL:inbox/jpg/d.jpg missing"; fail=1; fi
exit $fail
