#!/bin/bash
set -e
mkdir -p /root/sec/.github/workflows
cat > /root/sec/.github/workflows/sast.yml <<'YML'
name: SAST
on: [push]
jobs:
  semgrep:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Semgrep
        run: |
          pip install semgrep
          semgrep --config auto --error
YML
