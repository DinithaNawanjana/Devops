# Solution

```bash
mkdir -p /root/registry
cat > /root/registry/run.sh <<'SH'
#!/bin/bash
set -e
docker rm -f registry >/dev/null 2>&1 || true
docker run -d --name registry -p 5000:5000 registry:2
printf 'FROM alpine:3.19\nCMD ["echo","hi"]\n' > /root/registry/Dockerfile
docker build -t localhost:5000/demo:1 /root/registry
docker push localhost:5000/demo:1
SH
chmod +x /root/registry/run.sh
```
