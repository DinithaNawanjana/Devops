#!/bin/bash
set -e
mkdir -p /root/repo/.github/workflows
cat > /root/repo/.github/workflows/matrix.yml <<'YML'
name: Matrix
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        version: ["3.10", "3.11", "3.12"]
    steps:
      - run: echo "testing ${{ matrix.version }}"
YML
