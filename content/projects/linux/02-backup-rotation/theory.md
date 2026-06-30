# Deep Dive: Backups, Rotation & Retention

## The three jobs of a real backup script
1. **Capture** a consistent snapshot (here: a timestamped `tar.gz`).
2. **Rotate** — bound disk usage by keeping only the newest *N* archives.
3. **Log** — leave an audit trail so you can prove *when* a backup ran and
   whether it succeeded.

A backup you can't restore, or one that silently fills the disk and stops, is
worse than no backup because it creates false confidence.

## Timestamps that sort
Name archives `backup-$(date +%Y%m%d-%H%M%S).tar.gz`. The `YYYYMMDD-HHMMSS`
layout is **lexicographically sortable**, so `ls -1t` (by mtime) and a plain
alphabetical sort agree — which is what makes rotation reliable.

## The rotation one-liner, explained
```bash
ls -1t "$DEST"/backup-*.tar.gz | tail -n +$((KEEP+1)) | xargs -r rm -f
```
- `ls -1t` lists newest-first.
- `tail -n +$((KEEP+1))` skips the first `KEEP` (the keepers) and emits the rest.
- `xargs -r rm -f` deletes them; `-r` avoids running `rm` on empty input.

## Safety & idempotence
- `mkdir -p "$DEST"` so the first run can't fail on a missing directory.
- Fail loudly if the **source** is missing — never log "success" for an empty
  backup.
- `set -euo pipefail` so a failed `tar` aborts instead of rotating away good
  archives.

## Common pitfalls
- Backing up a live database with `tar` — you get a torn, inconsistent copy. Use
  the DB's dump tool (`pg_dump`, `mysqldump`) or snapshot the filesystem.
- Rotation counting *files in the dir* instead of *matching the glob* — stray
  files skew the count.

## Real-world
This pattern underlies `logrotate`, cron-driven DB dumps, and the retention
policies behind tools like restic, Velero, and cloud snapshot lifecycles.
