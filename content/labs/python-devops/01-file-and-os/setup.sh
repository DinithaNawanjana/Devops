#!/bin/sh
cd /root || exit 0
rm -f analyze.py summary.json
cat > access.log <<'EOF'
10.0.0.1 GET /index 200
10.0.0.2 GET /index 200
10.0.0.3 GET /about 404
10.0.0.1 POST /login 500
10.0.0.2 GET /index 200
10.0.0.4 GET /about 200
EOF
exit 0
