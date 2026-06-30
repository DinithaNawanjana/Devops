# Solution

```bash
mkdir -p /root/mc
for c in primary standby; do
cat > /root/mc/cluster-$c.yaml <<YML
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: $c
nodes:
  - role: control-plane
YML
done
cat > /root/mc/failover.sh <<'SH'
#!/bin/bash
set -euo pipefail
# Promote the standby cluster by switching context.
kubectl config use-context kind-standby
SH
chmod +x /root/mc/failover.sh
```
