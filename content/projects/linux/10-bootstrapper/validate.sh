#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0
[ -x ./bootstrap.sh ] || { echo "STEP:bootstrap.sh exists:FAIL:create executable /root/bootstrap.sh"; exit 1; }
echo "STEP:bootstrap.sh exists:PASS"
rm -rf myapp
./bootstrap.sh myapp >/dev/null 2>&1
if [ -d myapp/src ] && [ -d myapp/bin ] && [ -d myapp/config ]; then echo "STEP:creates src/bin/config:PASS"; else echo "STEP:creates src/bin/config:FAIL:missing directories"; fail=1; fi
if [ -f myapp/README.md ] && head -1 myapp/README.md | grep -q "myapp"; then echo "STEP:README mentions project name:PASS"; else echo "STEP:README mentions project name:FAIL:README.md first line should contain myapp"; fail=1; fi
ic=$(grep -c '^installed: ' myapp/installed.txt 2>/dev/null)
if [ "${ic:-0}" = "3" ] && grep -q '^installed: jq' myapp/installed.txt; then echo "STEP:installed.txt lists packages:PASS"; else echo "STEP:installed.txt lists packages:FAIL:need 3 'installed: <pkg>' lines"; fail=1; fi
exit $fail
