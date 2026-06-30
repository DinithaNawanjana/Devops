#!/bin/sh
F=/root/sec/Dockerfile
fail=0
[ -f "$F" ] && echo "STEP:Dockerfile exists:PASS" || { echo "STEP:Dockerfile exists:FAIL:create sec/Dockerfile"; exit 1; }
grep -qiE "alpine|slim|distroless" "$F" && echo "STEP:minimal base image:PASS" || { echo "STEP:minimal base image:FAIL:use alpine/slim/distroless"; fail=1; }
if grep -qE "^USER " "$F" && ! grep -qiE "^USER +root" "$F"; then echo "STEP:runs as non-root:PASS"; else echo "STEP:runs as non-root:FAIL:add a non-root USER"; fail=1; fi
exit $fail
