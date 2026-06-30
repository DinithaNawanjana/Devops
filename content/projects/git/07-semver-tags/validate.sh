#!/bin/sh
cd /root/repo 2>/dev/null || { echo "STEP:repo exists:FAIL:/root/repo missing"; exit 1; }
fail=0
if [ "$(git cat-file -t v1.0.0 2>/dev/null)" = "tag" ]; then echo "STEP:v1.0.0 annotated tag:PASS"; else echo "STEP:v1.0.0 annotated tag:FAIL:create annotated tag v1.0.0"; fail=1; fi
if [ "$(git cat-file -t v1.1.0 2>/dev/null)" = "tag" ]; then echo "STEP:v1.1.0 annotated tag:PASS"; else echo "STEP:v1.1.0 annotated tag:FAIL:create annotated tag v1.1.0"; fail=1; fi
d=$(git describe --tags 2>/dev/null)
if [ "$d" = "v1.1.0" ]; then echo "STEP:describe reports v1.1.0:PASS"; else echo "STEP:describe reports v1.1.0:FAIL:got '$d'"; fail=1; fi
exit $fail
