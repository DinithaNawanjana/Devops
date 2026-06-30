#!/bin/bash
set -e
mkdir -p /root/tf
cat > /root/tf/main.tf <<'TF'
resource "docker_container" "app" {
  name  = "app-${terraform.workspace}"
  image = "nginx:alpine"
}
TF
cat > /root/tf/setup-ws.sh <<'SH'
#!/bin/sh
for ws in dev stage prod; do terraform workspace new "$ws" 2>/dev/null || true; done
SH
chmod +x /root/tf/setup-ws.sh
