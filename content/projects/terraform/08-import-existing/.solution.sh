#!/bin/bash
set -e
mkdir -p /root/tf
cat > /root/tf/main.tf <<'TF'
resource "docker_container" "legacy" {
  name  = "legacy-app"
  image = "nginx:alpine"
}
TF
cat > /root/tf/import.sh <<'SH'
#!/bin/sh
# Bring the already-running container under management:
terraform import docker_container.legacy "$(docker ps -q --filter name=legacy-app)"
SH
chmod +x /root/tf/import.sh
