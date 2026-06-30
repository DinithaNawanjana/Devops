#!/bin/sh
F=/root/sec/sign.sh
fail=0
[ -x "$F" ] && echo "STEP:sign.sh exists:PASS" || { echo "STEP:sign.sh exists:FAIL:create executable sign.sh"; exit 1; }
grep -q "cosign sign" "$F" && echo "STEP:signs the image:PASS" || { echo "STEP:signs the image:FAIL:use cosign sign"; fail=1; }
grep -q "cosign verify" "$F" && echo "STEP:verifies the signature:PASS" || { echo "STEP:verifies the signature:FAIL:use cosign verify"; fail=1; }
exit $fail
