#!/bin/bash
set -e
mkdir -p /root/tf
cat > /root/tf/loops.tf <<'TF'
resource "docker_container" "workers" {
  count = 3
  name  = "worker-${count.index}"
  image = "nginx:alpine"
}

resource "docker_container" "services" {
  for_each = toset(["api", "web", "cache"])
  name     = each.key
  image    = "nginx:alpine"
}
TF
