# Solution

```bash
mkdir -p /root/k8s
cat > /root/k8s/isolation.yaml <<'YML'
apiVersion: v1
kind: Namespace
metadata: { name: team-a }
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata: { name: dev, namespace: team-a }
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata: { name: dev-binding, namespace: team-a }
subjects:
  - kind: User
    name: alice
roleRef:
  kind: Role
  name: dev
  apiGroup: rbac.authorization.k8s.io
---
apiVersion: v1
kind: ResourceQuota
metadata: { name: quota, namespace: team-a }
spec:
  hard:
    pods: "10"
    requests.cpu: "2"
YML
```
