#!/bin/bash
set -e
mkdir -p /root/repo/.github/workflows
cat > /root/repo/.github/workflows/secure.yml <<'YML'
name: Secure
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Registry login
        run: echo "${{ secrets.REGISTRY_TOKEN }}" | docker login -u ci --password-stdin
YML
