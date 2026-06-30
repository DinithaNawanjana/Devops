# Deep Dive: Multi-container Apps with Compose

## Why Compose exists
A real app is several processes — web, database, cache. Running each with a long
`docker run` line is error-prone and undocumented. **Compose** declares the whole
topology in one `docker-compose.yml`, version-controlled and reproducible:
`docker compose up` brings it all up.

## The mental model
Each `service` becomes one (or more) containers. Compose automatically creates a
**shared network** for the project, and — crucially — services reach each other
by **service name** as a DNS hostname (`web` can connect to `cache` at host
`cache`). No IPs, no links.

## Key fields
- `image` / `build` — where the container comes from.
- `ports: "8080:80"` — publish host:container (only needed for things you reach
  from outside).
- `depends_on` — start ordering (but *not* readiness — see pitfalls).
- `environment`, `volumes`, `networks`.

## Pitfalls
- `depends_on` waits for the container to **start**, not for the app inside to be
  **ready**. Use healthchecks + `condition: service_healthy` for true readiness.
- Publishing ports you don't need (DB on the host) — an attack surface.

## Real-world
Compose runs local dev environments, CI test stacks, and many small production
deployments; its model directly informs Kubernetes pods and services.
