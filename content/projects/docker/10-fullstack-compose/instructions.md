# Project Tasks

Write `/root/full/docker-compose.yml` with **four services**:

1. `frontend` and `backend` (any image, e.g. `nginx:alpine`).
2. `db` (e.g. `redis:7-alpine`).
3. `proxy` (`nginx:alpine`) that **publishes port 8080** and `depends_on` the
   frontend and backend.

```bash
cd /root/full
docker compose up -d
curl http://localhost:8080
```

Click **Check**.
