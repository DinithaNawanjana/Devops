# Solution

```bash
mkdir -p /root/k8s
cat > /root/k8s/config.yaml <<'YML'
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  LOG_LEVEL: info
YML
cat > /root/k8s/secret.yaml <<'YML'
apiVersion: v1
kind: Secret
metadata:
  name: app-secret
type: Opaque
stringData:
  API_KEY: s3cr3t
YML
cat > /root/k8s/pod.yaml <<'YML'
apiVersion: v1
kind: Pod
metadata:
  name: app
spec:
  containers:
    - name: app
      image: nginx:alpine
      envFrom:
        - configMapRef:
            name: app-config
        - secretRef:
            name: app-secret
YML
```
