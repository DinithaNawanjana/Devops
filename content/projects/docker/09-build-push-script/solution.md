# Solution

```bash
mkdir -p /root/cicd
printf 'FROM alpine:3.19\nCMD ["echo","app"]\n' > /root/cicd/Dockerfile
cat > /root/cicd/build.sh <<'SH'
#!/bin/bash
set -euo pipefail
IMAGE="${IMAGE:-localhost:5000/myapp}"
VERSION="${VERSION:-1.0.0}"
docker build -t "$IMAGE:$VERSION" .
docker push "$IMAGE:$VERSION"
SH
chmod +x /root/cicd/build.sh
```
