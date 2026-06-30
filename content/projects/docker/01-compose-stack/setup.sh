#!/bin/sh
cd /root || exit 0
# Clean any previous stack, leave the dir for the learner.
if [ -f stack/docker-compose.yml ]; then
  (cd stack && docker compose down >/dev/null 2>&1 || true)
fi
rm -rf stack
mkdir -p stack
exit 0
