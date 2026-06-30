#!/bin/sh
cd /root || exit 0
rm -rf platform
mkdir -p platform/.github/workflows platform/infra platform/k8s platform/monitoring platform/security
exit 0
