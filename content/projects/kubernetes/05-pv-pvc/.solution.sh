#!/bin/bash
set -e
mkdir -p /root/k8s
cat > /root/k8s/pvc.yaml <<'YML'
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data
spec:
  accessModes: ["ReadWriteOnce"]
  resources:
    requests:
      storage: 1Gi
YML
cat > /root/k8s/pod.yaml <<'YML'
apiVersion: v1
kind: Pod
metadata:
  name: stateful
spec:
  containers:
    - name: app
      image: nginx:alpine
      volumeMounts:
        - name: data
          mountPath: /data
  volumes:
    - name: data
      persistentVolumeClaim:
        claimName: data
YML
