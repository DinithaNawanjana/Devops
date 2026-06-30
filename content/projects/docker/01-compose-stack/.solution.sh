#!/bin/bash
set -e
mkdir -p /root/stack
cat > /root/stack/docker-compose.yml <<'YML'
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    depends_on:
      - cache
  cache:
    image: redis:7-alpine
YML
