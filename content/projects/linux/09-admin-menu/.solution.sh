#!/bin/bash
set -uo pipefail
while true; do
  echo "=== Admin Menu ==="
  echo "1) System time"
  echo "2) Disk usage"
  echo "3) Hostname"
  echo "q) Quit"
  read -r choice || break
  case "$choice" in
    1) echo "System time: $(date)" ;;
    2) echo "Disk usage: $(df -h / | awk 'NR==2{print $5}')" ;;
    3) echo "Hostname: $(hostname)" ;;
    q|Q) break ;;
    *) echo "unknown choice" ;;
  esac
done
