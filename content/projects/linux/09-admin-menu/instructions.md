# Project Tasks

Write `/root/admin.sh` — a loop that prints a menu and reads a choice each time:

- `1` → print a line starting with `System time:` followed by the date
- `2` → print a line starting with `Disk usage:` followed by `df` output
- `3` → print a line starting with `Hostname:` followed by the hostname
- `q` → quit

The menu listing must show the options (include `1)` and a quit hint). It must
read choices from **stdin** so it can be scripted, e.g.
`printf '1\nq\n' | ./admin.sh`. Then click **Check**.
