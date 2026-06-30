# Solution

`/root/stack/docker-compose.yml`:

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    depends_on:
      - cache
  cache:
    image: redis:7-alpine
```

Bring it up:

```bash
cd /root/stack
docker compose up -d
docker compose ps
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080   # 200
docker compose down    # when finished
```
