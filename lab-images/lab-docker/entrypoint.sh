#!/bin/sh
# Start an isolated Docker daemon for the sandbox, then hand off to CMD.
set -e

# Launch dockerd in the background (vfs is the most portable storage driver
# for nested setups; swap to overlay2 where the kernel allows it).
dockerd-entrypoint.sh dockerd \
    --storage-driver=vfs \
    >/var/log/dockerd.log 2>&1 &

# Wait for the daemon socket to come up (max ~30s).
i=0
while [ ! -S /var/run/docker.sock ] && [ "$i" -lt 30 ]; do
  i=$((i + 1))
  sleep 1
done

exec "$@"
