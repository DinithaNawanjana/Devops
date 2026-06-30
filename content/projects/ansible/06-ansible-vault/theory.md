# Project: Encrypted Secrets with Vault

`ansible-vault encrypt` turns a vars file into ciphertext (a file beginning with
`$ANSIBLE_VAULT;1.1;AES256`). A play loads it via `vars_files`.
