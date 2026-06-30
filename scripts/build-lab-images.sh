#!/usr/bin/env bash
# Build all lab sandbox base images. Run from the repo root.
#   ./scripts/build-lab-images.sh
set -euo pipefail

cd "$(dirname "$0")/.."

echo "▶ Building lab-linux:latest"
docker build -t lab-linux:latest lab-images/lab-linux

echo "▶ Building lab-docker:latest"
docker build -t lab-docker:latest lab-images/lab-docker

echo "▶ Building lab-ansible:latest"
docker build -t lab-ansible:latest lab-images/lab-ansible

echo "▶ Building lab-terraform:latest"
docker build -t lab-terraform:latest lab-images/lab-terraform

echo "✓ Lab images built:"
docker images | grep '^lab-' || true
