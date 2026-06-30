#!/bin/sh
fail=0
S=/root/ansible/secrets.yml
[ -f "$S" ] && head -1 "$S" | grep -q '\$ANSIBLE_VAULT' && echo "STEP:secrets.yml is vault-encrypted:PASS" || { echo "STEP:secrets.yml is vault-encrypted:FAIL:encrypt secrets.yml with ansible-vault"; fail=1; }
P=/root/ansible/vault.yml
[ -f "$P" ] && grep -q "vars_files:" "$P" && echo "STEP:play loads the vault file:PASS" || { echo "STEP:play loads the vault file:FAIL:reference secrets.yml via vars_files"; fail=1; }
exit $fail
