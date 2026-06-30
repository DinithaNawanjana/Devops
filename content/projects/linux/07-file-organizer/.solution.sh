#!/bin/bash
set -euo pipefail
cd /root/inbox
for f in *; do
  [ -f "$f" ] || continue          # skip directories
  ext="${f##*.}"
  [ "$ext" = "$f" ] && ext="noext"  # files without an extension
  mkdir -p "$ext"
  mv "$f" "$ext/"
done
