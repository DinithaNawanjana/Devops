#!/bin/bash
set -e
mkdir -p /root/sec
cat > /root/sec/policy.rego <<'REGO'
package main

deny[msg] {
  input.kind == "Deployment"
  some i
  image := input.spec.template.spec.containers[i].image
  endswith(image, ":latest")
  msg := sprintf("container image %v uses the latest tag", [image])
}
REGO
