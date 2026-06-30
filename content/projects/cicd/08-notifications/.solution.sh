#!/bin/bash
set -e
mkdir -p /root/repo/.github/workflows
cat > /root/repo/.github/workflows/notify.yml <<'YML'
name: Notify
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo build
      - name: Notify Slack
        if: always()
        run: curl -X POST -d 'text=build done' ${{ secrets.SLACK_WEBHOOK }}
YML
