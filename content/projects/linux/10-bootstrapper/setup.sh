#!/bin/sh
cd /root || exit 0
rm -rf myapp
cat > packages.txt <<'EOF'
curl
git
jq
EOF
exit 0
