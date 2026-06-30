# Solution

```bash
mkdir -p /root/tf
cat > /root/tf/backend.tf <<'TF'
terraform {
  backend "local" {
    path = "state/terraform.tfstate"
  }
}
TF
```
