# Project: System Info Dashboard

Build a portfolio-worthy Bash script that prints a clean system dashboard:
CPU, memory, and disk usage. This is the kind of script every sysadmin keeps
in their back pocket.

## Where the data lives

| Metric | Source |
|--------|--------|
| Hostname | `hostname` |
| Uptime | `uptime -p` or `/proc/uptime` |
| CPU model / cores | `/proc/cpuinfo`, `nproc` |
| Memory | `free -m` |
| Disk | `df -h /` |
| Load average | `/proc/loadavg` |

## Techniques you'll use

- Command substitution: `cpu=$(nproc)`
- `awk` to extract fields from `free`/`df`
- Here-documents and `printf` for aligned output
- Exit codes and a `--help` flag

Make the output readable — section headers, aligned columns. A good dashboard
is something you'd actually run every morning.
