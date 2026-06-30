#!/bin/bash
set -e
mkdir -p /root/sec/.github
cat > /root/sec/.github/dependabot.yml <<'YML'
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
YML
