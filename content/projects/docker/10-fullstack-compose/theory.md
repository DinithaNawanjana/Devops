# Deep Dive: Composing a Whole System

## From containers to architecture
This capstone of the Docker track wires four roles — frontend, backend, database,
and a reverse proxy — into one declarative stack. It's where Compose stops being
"run a container" and becomes "describe a system".

## The reverse proxy pattern
A proxy (nginx/Traefik/Caddy) is the single published entrypoint (`:8080`). It
routes paths/hosts to internal services that are **not** published to the host.
Benefits: one TLS termination point, path-based routing, and a smaller attack
surface (only the proxy is exposed).

## Ordering vs. readiness
`depends_on` sequences startup, but apps should still **retry** their
dependencies — a backend must tolerate the DB not accepting connections for the
first second. Healthchecks + `condition: service_healthy` tighten this.

## Pitfalls
- Publishing the DB/backend ports to the host "for debugging" and forgetting.
- Assuming start order equals ready order.
- One giant compose file with no profiles — split dev/prod concerns.

## Real-world
This four-tier shape (proxy → frontend/backend → datastore) is the canonical web
architecture; translating it to Kubernetes is Ingress → Services/Deployments →
StatefulSet, the same picture with cluster-grade primitives.
