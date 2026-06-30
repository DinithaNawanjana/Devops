# Solution

```bash
mkdir -p /root/tf
cat > /root/tf/main.tf <<'TF'
resource "null_resource" "configure" {
  provisioner "local-exec" {
    command = "ansible-playbook -i inventory.ini site.yml"
  }
}
TF
```
