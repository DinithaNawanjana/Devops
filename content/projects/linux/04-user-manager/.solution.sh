#!/bin/bash
set -euo pipefail
DB=/root/users.db
touch "$DB"
cmd="${1:-}"
case "$cmd" in
  add)
    user="$2"; full="$3"
    grep -q "^$user:" "$DB" || echo "$user:$full" >> "$DB" ;;
  del)
    user="$2"; sed -i "/^$user:/d" "$DB" ;;
  list) cat "$DB" ;;
  count) grep -c ':' "$DB" || true ;;
  *) echo "usage: usermgr.sh {add <u> <name>|del <u>|list|count}"; exit 1 ;;
esac
