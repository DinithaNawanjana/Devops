# Project: Backup Script with Rotation

A real backup script does three things well:

1. **Archives** a source directory (timestamped `tar.gz`).
2. **Rotates** old backups so the disk doesn't fill — keep only the newest N.
3. **Logs** every run so you can audit what happened.

## Key ideas

- Timestamps: `date +%Y%m%d-%H%M%S` for unique, sortable filenames.
- Archiving: `tar -czf backup-<ts>.tar.gz -C <src> .`
- Rotation: list backups newest-first, keep N, delete the rest:
  ```bash
  ls -1t "$DEST"/backup-*.tar.gz | tail -n +$((KEEP+1)) | xargs -r rm -f
  ```
- Logging: append `"$(date) message"` to a logfile; use a `log()` helper.

## Idempotence & safety

- Create the destination dir if missing (`mkdir -p`).
- Fail loudly if the source doesn't exist.
- Never delete more than rotation requires.
