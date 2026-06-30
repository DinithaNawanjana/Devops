#!/bin/sh
F=/root/sec/vault.sh
fail=0
[ -x "$F" ] && echo "STEP:vault.sh exists:PASS" || { echo "STEP:vault.sh exists:FAIL:create executable vault.sh"; exit 1; }
grep -q "vault kv put" "$F" && echo "STEP:stores a secret:PASS" || { echo "STEP:stores a secret:FAIL:use vault kv put"; fail=1; }
grep -q "vault kv get" "$F" && echo "STEP:retrieves a secret:PASS" || { echo "STEP:retrieves a secret:FAIL:use vault kv get"; fail=1; }
exit $fail
