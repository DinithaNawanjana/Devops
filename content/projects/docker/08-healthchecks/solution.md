# Solution

```bash
mkdir -p /root/health
cat > /root/health/docker-compose.yml <<'YML'
services:
  web:
    image: nginx:alpine
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost/"]
      interval: 5s
      timeout: 3s
      retries: 3
YML
```
