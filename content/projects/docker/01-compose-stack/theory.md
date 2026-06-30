# Project: Multi-Container App with Compose

Real apps are more than one container. **Docker Compose** declares a whole
stack in one `docker-compose.yml` and brings it up with a single command.

## Anatomy of a compose file

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

- **services** — each becomes a container
- **ports** — `HOST:CONTAINER` publishing
- **depends_on** — start ordering
- Compose creates a **shared network** so `web` can reach `cache` by name

## Commands

```bash
docker compose up -d        # create + start in the background
docker compose ps           # list the stack
docker compose logs web     # logs for one service
docker compose down         # stop + remove
```

Services on the same Compose network resolve each other by **service name**
(`cache`, `db`) — no IPs needed.
