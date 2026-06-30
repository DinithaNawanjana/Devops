#!/bin/bash
set -e
mkdir -p /root/sec/.github/workflows
cat > /root/sec/.github/workflows/scan.yml <<'YML'
name: Image Scan
on: [push]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:latest
          severity: HIGH,CRITICAL
          exit-code: '1'
YML
