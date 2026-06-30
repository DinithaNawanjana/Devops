#!/bin/bash
set -e
mkdir -p /root/tf
cat > /root/tf/main.tf <<'TF'
resource "docker_network" "appnet" {
  name = "appnet"
}

resource "docker_volume" "data" {
  name = "appdata"
}

resource "docker_container" "app" {
  name     = "app"
  image    = "nginx:alpine"
  networks_advanced { name = docker_network.appnet.name }
  volumes {
    volume_name    = docker_volume.data.name
    container_path = "/data"
  }
}

output "container_name" {
  value = docker_container.app.name
}
TF
