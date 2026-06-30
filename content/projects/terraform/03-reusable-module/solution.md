# Solution

```bash
mkdir -p /root/tf/modules/webserver
cat > /root/tf/modules/webserver/main.tf <<'TF'
variable "name" { type = string }
resource "docker_container" "this" {
  name  = var.name
  image = "nginx:alpine"
}
TF
cat > /root/tf/main.tf <<'TF'
module "web" {
  source = "./modules/webserver"
  name   = "web-1"
}
TF
```
