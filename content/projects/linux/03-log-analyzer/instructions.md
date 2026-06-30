# Project Tasks

`setup.sh` placed a log at `/root/logs/access.log` (fields: `ip method path status`).
Write `/root/loganalyze.sh` that creates a `/root/report/` directory with:

1. **`/root/report/total.txt`** — total number of log lines.
2. **`/root/report/error_count.txt`** — number of lines whose status is `500`.
3. **`/root/report/top_ips.txt`** — top 3 client IPs as `count ip`, busiest first.

Run `./loganalyze.sh`, inspect `/root/report/`, then click **Check**.
