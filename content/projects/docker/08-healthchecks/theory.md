# Deep Dive: Healthchecks & Restart Policies

## "Running" is not "healthy"
A container's process can be up while the app inside is deadlocked, still
booting, or out of connections. A **healthcheck** is a command Docker runs
periodically *inside* the container to test real behaviour, flipping its status
between `starting`, `healthy`, and `unhealthy`.

## Defining one
```yaml
healthcheck:
  test: ["CMD", "wget", "-qO-", "http://localhost/"]
  interval: 5s
  timeout: 3s
  retries: 3
  start_period: 10s
```
`start_period` gives slow-booting apps grace before failures count.

## Restart policies
`restart: unless-stopped` (or `always`) tells Docker to bring a crashed
container back. Combined with healthchecks and `depends_on:
condition: service_healthy`, you get dependency ordering that waits for real
readiness, not just process start.

## Pitfalls
- A healthcheck that always passes (e.g. checking the process, not the endpoint).
- Too-aggressive intervals hammering the app.
- `restart: always` masking a crash loop instead of fixing the cause.

## Real-world
This is the Compose-level version of Kubernetes liveness/readiness probes and
the foundation of zero-downtime rollouts.
