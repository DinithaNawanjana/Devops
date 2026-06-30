# Deep Dive: Persistence & Storage

## Containers are ephemeral
A container's writable layer dies with it. Anything you want to **outlive** the
container — database files, uploads — must live on a volume.

## Volumes vs. bind mounts
- **Named volume** (`docker volume create data`, `-v data:/var/lib/...`): Docker
  manages the storage location; portable, the right default for data.
- **Bind mount** (`-v /host/path:/in/container`): maps a host directory in;
  great for live-reloading source in dev, but ties you to the host layout.

## Why the lifecycle decoupling matters
You can destroy and recreate the container (upgrade the image, change flags) and
re-attach the same named volume — the data is untouched. That's what makes
stateful containers (databases) viable.

## Pitfalls
- Writing data into the container filesystem instead of the volume → lost on
  recreate.
- Two containers writing the same volume without coordination → corruption (most
  databases assume single-writer).
- Forgetting volumes persist after `docker rm` — `docker volume prune` to clean.

## Real-world
Postgres/MySQL containers, upload stores, and CI caches all rely on volumes; in
Kubernetes the same idea becomes PersistentVolumes/PVCs.
