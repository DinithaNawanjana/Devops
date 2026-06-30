# Solution

```bash
cat > /root/backup.sh <<'SCRIPT'
#!/bin/bash
set -euo pipefail

SRC="/root/data"
DEST="/root/backups"
KEEP=3
LOG="$DEST/backup.log"

mkdir -p "$DEST"
log() { echo "$(date '+%F %T') $*" >> "$LOG"; }

if [ ! -d "$SRC" ]; then
  log "ERROR: source $SRC missing"
  echo "source missing" >&2
  exit 1
fi

TS=$(date +%Y%m%d-%H%M%S)
ARCHIVE="$DEST/backup-$TS.tar.gz"
tar -czf "$ARCHIVE" -C "$SRC" .
log "created $ARCHIVE"

# Rotation: keep the newest $KEEP, delete the rest.
ls -1t "$DEST"/backup-*.tar.gz | tail -n +$((KEEP + 1)) | while read -r old; do
  rm -f "$old"
  log "rotated out $old"
done
SCRIPT

chmod 755 /root/backup.sh

# Run it a few times
for i in 1 2 3 4 5; do /root/backup.sh; sleep 1; done
ls -1 /root/backups
```
