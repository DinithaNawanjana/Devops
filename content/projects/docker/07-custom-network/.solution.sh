#!/bin/bash
set -e
mkdir -p /root/net
cat > /root/net/docker-compose.yml <<'YML'
services:
  web:
    image: nginx:alpine
    networks: [appnet]
  api:
    image: nginx:alpine
    networks: [appnet]
  cache:
    image: redis:7-alpine
    networks: [appnet]
networks:
  appnet:
YML
