#!/bin/bash
set -e
mkdir -p /root/repo/.github/workflows
cat > /root/repo/.github/workflows/ci.yml <<'YML'
name: CI
on:
  push:
  pull_request:
jobs:
  lint-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Lint
        run: flake8 .
      - name: Test
        run: pytest -q
YML
