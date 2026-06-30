#!/bin/sh
cd /root/app 2>/dev/null || { echo "STEP:app repo exists:FAIL:/root/app missing"; exit 1; }
fail=0
if [ -f .gitmodules ] && grep -q "vendor/lib" .gitmodules; then echo "STEP:.gitmodules references vendor/lib:PASS"; else echo "STEP:.gitmodules references vendor/lib:FAIL:add submodule at vendor/lib"; fail=1; fi
if [ -f vendor/lib/lib.txt ] && grep -q "lib v1" vendor/lib/lib.txt; then echo "STEP:submodule content checked out:PASS"; else echo "STEP:submodule content checked out:FAIL:vendor/lib/lib.txt missing"; fail=1; fi
exit $fail
