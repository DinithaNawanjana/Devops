# Solution

```bash
mkdir -p /root/idp
cat > /root/idp/catalog-info.yaml <<'YML'
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: checkout
  annotations:
    backstage.io/techdocs-ref: dir:.
spec:
  type: service
  lifecycle: production
  owner: team-a
YML
cat > /root/idp/template.yaml <<'YML'
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: node-service
spec:
  type: service
  parameters: []
  steps: []
YML
```
