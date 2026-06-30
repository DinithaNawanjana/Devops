#!/bin/bash
set -euo pipefail
mkdir -p /root/run
MARK=/root/run/service.up
LOG=/root/run/watch.log
if [ ! -f "$MARK" ]; then
  touch "$MARK"
  echo "$(date '+%F %T') service down -> restart" >> "$LOG"
else
  echo "$(date '+%F %T') service ok" >> "$LOG"
fi
