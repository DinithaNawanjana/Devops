#!/bin/bash
set -e
mkdir -p /root/repo/.github/workflows
cat > /root/repo/.github/workflows/pipeline.yml <<'YML'
name: Pipeline
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo build
  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo test
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: echo deploy
YML
