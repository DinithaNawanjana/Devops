#!/bin/bash
set -e
mkdir -p /root/full
cat > /root/full/docker-compose.yml <<'YML'
services:
  frontend:
    image: nginx:alpine
  backend:
    image: nginx:alpine
  db:
    image: redis:7-alpine
  proxy:
    image: nginx:alpine
    ports:
      - "8080:80"
    depends_on:
      - frontend
      - backend
YML
