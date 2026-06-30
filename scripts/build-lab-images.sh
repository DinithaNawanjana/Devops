#!/usr/bin/env bash
# Build all lab sandbox base images. Run from the repo root.
#   ./scripts/build-lab-images.sh
set -euo pipefail

cd "$(dirname "$0")/.."

echo "▶ Building lab-linux:latest"
docker build -t lab-linux:latest lab-images/lab-linux

echo "▶ Building lab-docker:latest"
docker build -t lab-docker:latest lab-images/lab-docker

echo "✓ Lab images built:"
docker images | grep '^lab-' || true
