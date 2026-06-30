#!/bin/bash
set -e
mkdir -p /root/tf
cat > /root/tf/variables.tf <<'TF'
variable "container_name" {
  type    = string
  default = "app"
}
variable "external_port" {
  type    = number
  default = 8080
}
TF
cat > /root/tf/outputs.tf <<'TF'
output "url" {
  value = "http://localhost:${var.external_port}"
}
TF
cat > /root/tf/terraform.tfvars <<'TF'
container_name = "myapp"
external_port  = 9090
TF
