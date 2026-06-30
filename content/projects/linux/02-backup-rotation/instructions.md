# Project Tasks

Write `/root/backup.sh` that backs up `/root/data` into `/root/backups`,
keeping only the **3 newest** archives, and logs to `/root/backups/backup.log`.

`setup.sh` has created a sample `/root/data` directory for you.

Requirements:

1. **Executable** `/root/backup.sh` (mode `755`, `#!/bin/bash` shebang).

2. **Creates a timestamped archive** in `/root/backups/` named
   `backup-<timestamp>.tar.gz` containing the contents of `/root/data`.

3. **Rotation** — after running the script **5 times**, only the **3 newest**
   `backup-*.tar.gz` files remain in `/root/backups/`.

4. **Logging** — each run appends a line to `/root/backups/backup.log`.

Run your script a few times (e.g. `for i in 1 2 3 4 5; do ./backup.sh; sleep 1; done`),
then click **Check**.

> The checker runs your script 5 times itself, then verifies the count.
