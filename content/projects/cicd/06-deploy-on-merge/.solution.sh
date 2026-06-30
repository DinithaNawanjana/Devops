#!/bin/bash
set -e
mkdir -p /root/repo/.github/workflows
cat > /root/repo/.github/workflows/deploy.yml <<'YML'
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Publish to nginx
        run: cp -r site/* /usr/share/nginx/html/
YML
