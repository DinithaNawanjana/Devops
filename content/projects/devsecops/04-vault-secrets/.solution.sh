#!/bin/bash
set -e
mkdir -p /root/sec
cat > /root/sec/vault.sh <<'SH'
#!/bin/bash
set -euo pipefail
export VAULT_ADDR="http://127.0.0.1:8200"
# Store
vault kv put secret/myapp db_password=s3cr3t
# Retrieve
vault kv get -field=db_password secret/myapp
SH
chmod +x /root/sec/vault.sh
