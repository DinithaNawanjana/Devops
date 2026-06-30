#!/bin/sh
cd /root || exit 0
rm -rf report logs
mkdir -p logs
cat > logs/access.log <<'EOF'
10.0.0.1 GET /a 200
10.0.0.2 GET /b 200
10.0.0.1 GET /a 500
10.0.0.1 GET /c 200
10.0.0.3 GET /d 404
10.0.0.2 GET /e 500
EOF
exit 0
