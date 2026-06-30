#!/bin/bash
set -e
mkdir -p /root/site/html
echo "<h1>Hello Docker</h1>" > /root/site/html/index.html
cat > /root/site/Dockerfile <<'DF'
FROM nginx:alpine
COPY html/ /usr/share/nginx/html/
DF
