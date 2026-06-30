#!/bin/bash
set -e
mkdir -p /root/sec
cat > /root/sec/sign.sh <<'SH'
#!/bin/bash
set -euo pipefail
IMAGE="localhost:5000/myapp:1.0.0"
cosign sign --key cosign.key "$IMAGE"
cosign verify --key cosign.pub "$IMAGE"
SH
chmod +x /root/sec/sign.sh
