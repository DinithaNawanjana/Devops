# Solution

```bash
mkdir -p /root/k8s
cat > /root/k8s/pod.yaml <<'YML'
apiVersion: v1
kind: Pod
metadata:
  name: web
  labels:
    app: web
spec:
  containers:
    - name: nginx
      image: nginx:alpine
      ports:
        - containerPort: 80
YML
cat > /root/k8s/service.yaml <<'YML'
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  selector:
    app: web
  ports:
    - port: 80
      targetPort: 80
YML
```
