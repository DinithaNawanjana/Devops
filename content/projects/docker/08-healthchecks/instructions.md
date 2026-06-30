# Project Tasks

Write `/root/health/docker-compose.yml` with a `web` service (`nginx:alpine`)
that has:

1. A **`healthcheck`** with a `test` command that probes the server.
2. A **`restart`** policy of `unless-stopped` (or `always`).

```bash
cd /root/health
docker compose up -d
docker compose ps      # shows (healthy) once probes pass
```

Click **Check**.
