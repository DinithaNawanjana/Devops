# Deep Dive: Container Networking & Service Discovery

## The default isn't enough
On the default bridge, containers can talk by IP but **not by name**. The moment
you have more than one service, you want a **user-defined network**, which adds
an embedded DNS so containers resolve each other by **name**.

## How discovery works
On a user-defined network (which Compose creates for you), service `web` can
`curl http://api` and Docker's DNS resolves `api` to that container's current
IP — even across restarts when the IP changes. This is why you never hardcode
container IPs.

## Segmentation
Multiple networks let you isolate tiers: put the database on a `backend` network
the frontend can't reach, exposing only what's necessary. Least privilege at the
network layer.

## Pitfalls
- Relying on the default bridge and wondering why name resolution fails.
- Publishing internal services to the host (`-p`) when only other containers
  need them.
- Assuming containers on *different* networks can talk — they can't unless
  attached to a common one.

## Real-world
This DNS-by-name model is exactly how Kubernetes Services work; learning it in
Compose makes K8s networking click.
