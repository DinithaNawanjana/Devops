# Project Tasks

Write `/root/net/docker-compose.yml` with **three services** — `web`, `api`,
`cache` — all attached to a **custom network** named `appnet`.

- `web` and `api`: `nginx:alpine`
- `cache`: `redis:7-alpine`

```bash
cd /root/net
docker compose up -d
docker compose ps
```

Click **Check**.
