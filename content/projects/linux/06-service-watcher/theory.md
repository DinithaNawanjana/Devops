# Deep Dive: Health Checks & Self-Healing

## Liveness, then remediation
A watchdog does two things: **detect** that a service is unhealthy, and
**remediate** (restart it). Modelling the service as a marker file keeps the
focus on the control loop rather than on process plumbing — but the logic maps
directly onto checking a PID, a port, or an HTTP endpoint.

## The control loop
```
observe current state  ->  compare to desired (up)  ->  if drifted, act  ->  log
```
This **observe/diff/act** loop is the same reconciliation pattern Kubernetes
controllers run continuously. Your script is a one-shot reconciler; cron makes
it periodic.

## Detecting real services
Swap the marker check for any of:
- `pgrep -x nginx` — is the process running?
- `nc -z localhost 80` — is the port accepting connections?
- `curl -fsS localhost/health` — does the app say it's healthy?

The last is best: a process can be *running* but *wedged*. Liveness should test
behaviour, not mere existence.

## Logging events, not spam
Log a `restart` only on transitions, `ok` otherwise, so the log reads like an
incident timeline rather than noise.

## Common pitfalls
- Restart loops: if the service crashes instantly, a naive watcher hot-loops.
  Real supervisors add backoff and a crash-count ceiling.
- Treating "process exists" as "healthy".

## Real-world
This is `systemd` `Restart=on-failure`, Docker `--restart`, and Kubernetes
liveness probes, distilled to its essence.
