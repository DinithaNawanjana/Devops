#!/bin/sh
# Seed a deterministic sample access log.
cd /root || exit 0
rm -f total.txt errors.txt top_ips.txt
cat > access.log <<'EOF'
10.0.0.1 GET /index.html 200
10.0.0.2 GET /about.html 200
10.0.0.1 GET /contact.html 200
10.0.0.3 POST /login ERROR
10.0.0.1 GET /index.html 200
10.0.0.2 GET /style.css 200
10.0.0.1 GET /app.js 500 ERROR
10.0.0.4 GET /missing 404 ERROR
10.0.0.2 GET /index.html 200
10.0.0.1 GET /favicon.ico 200
EOF
exit 0
