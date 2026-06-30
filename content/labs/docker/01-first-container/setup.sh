#!/bin/sh
# Ensure a clean slate. The dind daemon is started by the image entrypoint.
cd /root || exit 0
rm -f container_id.txt
# Best-effort: remove a leftover web container from a previous attempt.
docker rm -f web >/dev/null 2>&1 || true
exit 0
