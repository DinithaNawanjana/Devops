# Solution

```bash
mkdir -p /root/gitops/chart
cat > /root/gitops/chart/Chart.yaml <<'YML'
apiVersion: v2
name: app
version: 0.1.0
YML
for env in dev prod; do
cat > /root/gitops/app-$env.yaml <<YML
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: app-$env
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/example/app.git
    path: chart
    helm:
      valueFiles: [values-$env.yaml]
  destination:
    server: https://kubernetes.default.svc
    namespace: $env
  syncPolicy:
    automated: { prune: true, selfHeal: true }
YML
done
```
