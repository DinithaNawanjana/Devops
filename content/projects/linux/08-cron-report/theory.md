# Deep Dive: Scheduling with cron

## Two halves of a scheduled job
A scheduled task is a **payload** (the script that does the work) plus a
**schedule** (when cron runs it). Keeping them separate — a clean `genreport.sh`
and a one-line crontab entry — makes the payload testable on its own.

## Reading a crontab line
```
0 6 * * *  /root/genreport.sh
│ │ │ │ │
│ │ │ │ └── day of week (0-6, Sun=0)
│ │ │ └──── month (1-12)
│ │ └────── day of month (1-31)
│ └──────── hour (0-23)
└────────── minute (0-59)
```
`0 6 * * *` = 06:00 every day. `*/15 * * * *` = every 15 minutes. `@daily`,
`@reboot` are shorthands.

## Why cron scripts break in production
cron runs with a **minimal environment**: a short `PATH`, no `~/.bashrc`, often
`/bin/sh` not Bash, and `HOME` possibly unset. Scripts that work in your
interactive shell fail under cron because of this. Defenses:
- Use **absolute paths** for binaries and files.
- Set `PATH` explicitly at the top of the script.
- Redirect output (`>> log 2>&1`) — cron emails stdout by default, which often
  silently black-holes.

## Common pitfalls
- Relative paths (cron's CWD is `$HOME`, not where the script lives).
- Assuming Bash features under `/bin/sh`.
- Forgetting that `%` is special in crontab lines (must be escaped).

## Real-world
Cron still drives backups, certificate renewals, report generation, and cleanup
jobs everywhere; Kubernetes `CronJob` borrows the exact schedule syntax.
