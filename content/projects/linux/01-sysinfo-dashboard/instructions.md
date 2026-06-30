# Project Tasks

Build `/root/sysinfo.sh`. Requirements:

1. **Executable script** at `/root/sysinfo.sh`, mode `755`, starting with a
   `#!/bin/bash` shebang.

2. **Sections** — when run, the output must contain these section headers
   (case-insensitive), each followed by real data:
   - `HOSTNAME`
   - `CPU`
   - `MEMORY`
   - `DISK`

3. **Memory data** — include the total memory (e.g. derived from `free -m`).

4. **Disk data** — include the usage of `/` (e.g. from `df -h /`).

5. **Help flag** — running `./sysinfo.sh --help` must print a usage line
   containing the word `usage` and exit `0` without printing the dashboard.

Build it, run `./sysinfo.sh`, then click **Check**.

> Tip: keep a `print_section()` helper to stay DRY.
