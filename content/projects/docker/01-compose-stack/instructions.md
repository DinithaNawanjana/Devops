# Project Tasks

Build a two-service stack in `/root/stack/docker-compose.yml`.

Requirements:

1. **Compose file** at `/root/stack/docker-compose.yml`.

2. **A `web` service** using `nginx:alpine`, publishing host port **8080** to
   container port **80**.

3. **A `cache` service** using `redis:7-alpine`.

4. **Both running** — after `docker compose up -d` from `/root/stack`, both the
   `web` and `cache` containers are up.

5. **Web reachable** — `curl http://localhost:8080` returns HTTP `200`.

Bring it up yourself to test:

```bash
cd /root/stack
docker compose up -d
docker compose ps
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8080
```

Then click **Check** (the checker will `up -d` the stack itself before
verifying).
