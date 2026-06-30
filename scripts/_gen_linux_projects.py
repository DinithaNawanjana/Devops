#!/usr/bin/env python3
"""One-off authoring helper: write the Linux & Bash project set (03-10).

Each project gets the standard folder format. `_solution_cmds` is the reference
implementation, embedded into solution.md AND used by the test harness
(scripts/_test_linux_projects.sh) to verify each validate.sh passes.
"""
import os
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "content" / "projects" / "linux"

PROJECTS = []


def proj(**kw):
    PROJECTS.append(kw)


# ── 03 Log analyzer ──────────────────────────────────────
proj(
    dir="03-log-analyzer", id="proj-linux-loganalyzer",
    title="Project: Log File Analyzer", minutes=45, points=250,
    prereq="[bash-01]",
    theory="""# Project: Log File Analyzer

Parse a web access log with `grep`/`awk`/`sort`/`uniq` and emit a report:
total requests, error count, and the busiest client IPs. This is the bread and
butter of incident triage.

Key recipe — top N by frequency:

```bash
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -3
```
""",
    instructions="""# Project Tasks

`setup.sh` placed a log at `/root/logs/access.log` (fields: `ip method path status`).
Write `/root/loganalyze.sh` that creates a `/root/report/` directory with:

1. **`/root/report/total.txt`** — total number of log lines.
2. **`/root/report/error_count.txt`** — number of lines whose status is `500`.
3. **`/root/report/top_ips.txt`** — top 3 client IPs as `count ip`, busiest first.

Run `./loganalyze.sh`, inspect `/root/report/`, then click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf report logs
mkdir -p logs
cat > logs/access.log <<'EOF'
10.0.0.1 GET /a 200
10.0.0.2 GET /b 200
10.0.0.1 GET /a 500
10.0.0.1 GET /c 200
10.0.0.3 GET /d 404
10.0.0.2 GET /e 500
EOF
exit 0
""",
    validate="""#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0
[ -x ./loganalyze.sh ] || { echo "STEP:loganalyze.sh exists:FAIL:create executable /root/loganalyze.sh"; exit 1; }
echo "STEP:loganalyze.sh exists:PASS"
./loganalyze.sh >/dev/null 2>&1
total=$(tr -dc '0-9' < report/total.txt 2>/dev/null)
if [ "$total" = "6" ]; then echo "STEP:total is 6:PASS"; else echo "STEP:total is 6:FAIL:got '$total'"; fail=1; fi
err=$(tr -dc '0-9' < report/error_count.txt 2>/dev/null)
if [ "$err" = "2" ]; then echo "STEP:error_count is 2:PASS"; else echo "STEP:error_count is 2:FAIL:got '$err'"; fail=1; fi
l1=$(sed -n '1p' report/top_ips.txt 2>/dev/null)
if echo "$l1" | grep -q "3" && echo "$l1" | grep -q "10.0.0.1"; then
  echo "STEP:top IP is 10.0.0.1 (3):PASS"; else echo "STEP:top IP is 10.0.0.1 (3):FAIL:top_ips.txt first line wrong"; fail=1; fi
exit $fail
""",
    solution="""#!/bin/bash
set -euo pipefail
mkdir -p /root/report
LOG=/root/logs/access.log
wc -l < "$LOG" > /root/report/total.txt
awk '$4==500' "$LOG" | wc -l > /root/report/error_count.txt
awk '{print $1}' "$LOG" | sort | uniq -c | sort -rn | head -3 > /root/report/top_ips.txt
""",
)

# ── 04 User manager ──────────────────────────────────────
proj(
    dir="04-user-manager", id="proj-linux-usermgr",
    title="Project: User Account Manager", minutes=50, points=300,
    prereq="[proj-linux-loganalyzer]",
    theory="""# Project: User Account Manager

A menu of subcommands that manage a simple user database file
(`/root/users.db`, one `user:fullname` per line). Practises argument parsing,
`case` statements, idempotent edits, and `grep`/`sed`.
""",
    instructions="""# Project Tasks

Write `/root/usermgr.sh` operating on `/root/users.db` (created empty by setup).
Support these subcommands:

1. **`add <user> <fullname>`** — append `user:fullname` **only if the user
   doesn't already exist** (idempotent).
2. **`del <user>`** — remove that user's line.
3. **`list`** — print the database.
4. **`count`** — print the number of users (just the number).

Example: `./usermgr.sh add alice "Alice A"`. Then click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -f users.db
: > users.db
exit 0
""",
    validate="""#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0
[ -x ./usermgr.sh ] || { echo "STEP:usermgr.sh exists:FAIL:create executable /root/usermgr.sh"; exit 1; }
echo "STEP:usermgr.sh exists:PASS"
: > users.db
./usermgr.sh add alice "Alice A" >/dev/null 2>&1
./usermgr.sh add bob "Bob B"   >/dev/null 2>&1
./usermgr.sh add alice "Alice A" >/dev/null 2>&1   # duplicate, must be ignored
n=$(./usermgr.sh count 2>/dev/null | tr -dc '0-9')
if [ "$n" = "2" ]; then echo "STEP:add is idempotent (count=2):PASS"; else echo "STEP:add is idempotent (count=2):FAIL:got count '$n'"; fail=1; fi
if grep -q "^alice:" users.db; then echo "STEP:alice stored:PASS"; else echo "STEP:alice stored:FAIL:alice not in users.db"; fail=1; fi
./usermgr.sh del bob >/dev/null 2>&1
if ! grep -q "^bob:" users.db; then echo "STEP:del removes bob:PASS"; else echo "STEP:del removes bob:FAIL:bob still present"; fail=1; fi
n2=$(./usermgr.sh count 2>/dev/null | tr -dc '0-9')
if [ "$n2" = "1" ]; then echo "STEP:count after delete is 1:PASS"; else echo "STEP:count after delete is 1:FAIL:got '$n2'"; fail=1; fi
exit $fail
""",
    solution="""#!/bin/bash
set -euo pipefail
DB=/root/users.db
touch "$DB"
cmd="${1:-}"
case "$cmd" in
  add)
    user="$2"; full="$3"
    grep -q "^$user:" "$DB" || echo "$user:$full" >> "$DB" ;;
  del)
    user="$2"; sed -i "/^$user:/d" "$DB" ;;
  list) cat "$DB" ;;
  count) grep -c ':' "$DB" || true ;;
  *) echo "usage: usermgr.sh {add <u> <name>|del <u>|list|count}"; exit 1 ;;
esac
""",
)

# ── 05 Disk alert ────────────────────────────────────────
proj(
    dir="05-disk-alert", id="proj-linux-diskalert",
    title="Project: Disk Usage Alert", minutes=40, points=250,
    prereq="[proj-linux-usermgr]",
    theory="""# Project: Disk Usage Alert

Read the root filesystem usage from `df` and raise an alert when it crosses a
threshold. Practises `df` parsing, numeric comparison, and logging.

```bash
df -P / | awk 'NR==2{gsub("%","",$5); print $5}'   # usage as a number
```
""",
    instructions="""# Project Tasks

Write `/root/diskalert.sh <threshold>` that:

1. Reads the **current `/` usage percentage** from `df`.
2. If usage **> threshold**, writes `ALERT` (plus the percentage) to
   `/root/alert.txt`; otherwise writes `OK`.
3. **Appends a line to `/root/alert.log`** on every run.

Test both branches: `./diskalert.sh 0` (should ALERT) and
`./diskalert.sh 100` (should be OK). Then click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -f alert.txt alert.log
exit 0
""",
    validate="""#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0
[ -x ./diskalert.sh ] || { echo "STEP:diskalert.sh exists:FAIL:create executable /root/diskalert.sh"; exit 1; }
echo "STEP:diskalert.sh exists:PASS"
: > alert.log
./diskalert.sh 0 >/dev/null 2>&1
if grep -q "ALERT" alert.txt 2>/dev/null; then echo "STEP:threshold 0 triggers ALERT:PASS"; else echo "STEP:threshold 0 triggers ALERT:FAIL:alert.txt should say ALERT"; fail=1; fi
./diskalert.sh 100 >/dev/null 2>&1
if grep -q "OK" alert.txt 2>/dev/null; then echo "STEP:threshold 100 is OK:PASS"; else echo "STEP:threshold 100 is OK:FAIL:alert.txt should say OK"; fail=1; fi
lines=$(grep -c . alert.log 2>/dev/null)
if [ "${lines:-0}" -ge 2 ]; then echo "STEP:logs every run:PASS"; else echo "STEP:logs every run:FAIL:alert.log should have a line per run"; fail=1; fi
exit $fail
""",
    solution="""#!/bin/bash
set -euo pipefail
threshold="${1:-80}"
usage=$(df -P / | awk 'NR==2{gsub("%","",$5); print $5}')
if [ "$usage" -gt "$threshold" ]; then
  echo "ALERT: / at ${usage}% (>${threshold}%)" > /root/alert.txt
else
  echo "OK: / at ${usage}% (<=${threshold}%)" > /root/alert.txt
fi
echo "$(date '+%F %T') usage=${usage}% threshold=${threshold}%" >> /root/alert.log
""",
)

# ── 06 Service watcher ───────────────────────────────────
proj(
    dir="06-service-watcher", id="proj-linux-watcher",
    title="Project: Service Health Watcher", minutes=50, points=300,
    prereq="[proj-linux-diskalert]",
    theory="""# Project: Service Health Watcher

A watchdog that checks whether a service is up and restarts it if not. Here the
"service" is represented by the marker file `/root/run/service.up`. Practises
existence checks, recreating state, and event logging.
""",
    instructions="""# Project Tasks

Write `/root/watch.sh`. On each run it must:

1. Check whether `/root/run/service.up` exists (the "service is running" marker).
2. **If missing** — recreate it and append a line containing `restart` to
   `/root/run/watch.log`.
3. **If present** — append a line containing `ok` to `/root/run/watch.log`.

The checker will delete the marker, run your script (expecting a restart), then
run it again (expecting ok). Click **Check** when ready.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf run
mkdir -p run
exit 0
""",
    validate="""#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0
[ -x ./watch.sh ] || { echo "STEP:watch.sh exists:FAIL:create executable /root/watch.sh"; exit 1; }
echo "STEP:watch.sh exists:PASS"
mkdir -p run; : > run/watch.log; rm -f run/service.up
./watch.sh >/dev/null 2>&1
if [ -f run/service.up ]; then echo "STEP:recreates missing service marker:PASS"; else echo "STEP:recreates missing service marker:FAIL:service.up not recreated"; fail=1; fi
if grep -qi "restart" run/watch.log; then echo "STEP:logs a restart event:PASS"; else echo "STEP:logs a restart event:FAIL:watch.log has no restart entry"; fail=1; fi
./watch.sh >/dev/null 2>&1
if grep -qi "ok" run/watch.log; then echo "STEP:logs ok when healthy:PASS"; else echo "STEP:logs ok when healthy:FAIL:second run should log ok"; fail=1; fi
exit $fail
""",
    solution="""#!/bin/bash
set -euo pipefail
mkdir -p /root/run
MARK=/root/run/service.up
LOG=/root/run/watch.log
if [ ! -f "$MARK" ]; then
  touch "$MARK"
  echo "$(date '+%F %T') service down -> restart" >> "$LOG"
else
  echo "$(date '+%F %T') service ok" >> "$LOG"
fi
""",
)

# ── 07 File organizer ────────────────────────────────────
proj(
    dir="07-file-organizer", id="proj-linux-organizer",
    title="Project: File Organizer by Extension", minutes=40, points=250,
    prereq="[proj-linux-watcher]",
    theory="""# Project: File Organizer

Tidy a messy directory by moving each file into a subfolder named after its
extension. Practises globbing, parameter expansion (`${f##*.}`), and `mv`.
""",
    instructions="""# Project Tasks

`setup.sh` filled `/root/inbox/` with mixed files. Write `/root/organize.sh`
that moves each **file** in `/root/inbox/` into a subdirectory named after its
extension, e.g. `a.txt` → `/root/inbox/txt/a.txt`, `c.log` → `/root/inbox/log/c.log`.

Already-organized subdirectories must be left alone. Run it, then click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf inbox
mkdir -p inbox
cd inbox
for f in a.txt b.txt e.txt; do echo data > "$f"; done
echo log > c.log
echo img > d.jpg
exit 0
""",
    validate="""#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0
[ -x ./organize.sh ] || { echo "STEP:organize.sh exists:FAIL:create executable /root/organize.sh"; exit 1; }
echo "STEP:organize.sh exists:PASS"
./organize.sh >/dev/null 2>&1
txt=$(ls inbox/txt 2>/dev/null | grep -c .)
if [ "${txt:-0}" = "3" ]; then echo "STEP:txt files grouped (3):PASS"; else echo "STEP:txt files grouped (3):FAIL:inbox/txt should hold 3 files, found ${txt:-0}"; fail=1; fi
if [ -f inbox/log/c.log ]; then echo "STEP:log file grouped:PASS"; else echo "STEP:log file grouped:FAIL:inbox/log/c.log missing"; fail=1; fi
if [ -f inbox/jpg/d.jpg ]; then echo "STEP:jpg file grouped:PASS"; else echo "STEP:jpg file grouped:FAIL:inbox/jpg/d.jpg missing"; fail=1; fi
exit $fail
""",
    solution="""#!/bin/bash
set -euo pipefail
cd /root/inbox
for f in *; do
  [ -f "$f" ] || continue          # skip directories
  ext="${f##*.}"
  [ "$ext" = "$f" ] && ext="noext"  # files without an extension
  mkdir -p "$ext"
  mv "$f" "$ext/"
done
""",
)

# ── 08 Cron report ───────────────────────────────────────
proj(
    dir="08-cron-report", id="proj-linux-cronreport",
    title="Project: Scheduled Report Generator", minutes=45, points=250,
    prereq="[proj-linux-organizer]",
    theory="""# Project: Scheduled Report Generator

Generate a dated report and define the cron schedule that would run it. A cron
line is five time fields plus a command:

```
0 6 * * *  /root/genreport.sh    # every day at 06:00
```
""",
    instructions="""# Project Tasks

Write `/root/genreport.sh` that:

1. Creates `/root/reports/` and writes a dated report file
   `report-<YYYY-MM-DD>.txt` containing a line `Files: <N>` where `<N>` is the
   number of files in `/root/data/` (created by setup).
2. Writes a **valid cron line** to `/root/reports/crontab.txt` — five schedule
   fields followed by a command that mentions `genreport.sh` (e.g. run daily).

Run `./genreport.sh`, then click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf reports data
mkdir -p data
echo a > data/one; echo b > data/two; echo c > data/three
exit 0
""",
    validate="""#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0
[ -x ./genreport.sh ] || { echo "STEP:genreport.sh exists:FAIL:create executable /root/genreport.sh"; exit 1; }
echo "STEP:genreport.sh exists:PASS"
./genreport.sh >/dev/null 2>&1
rep=$(ls reports/report-*.txt 2>/dev/null | head -1)
if [ -n "$rep" ] && grep -q "Files: 3" "$rep"; then echo "STEP:dated report says Files: 3:PASS"; else echo "STEP:dated report says Files: 3:FAIL:report-<date>.txt should contain 'Files: 3'"; fail=1; fi
if grep -Eq '^[0-9*/,-]+ +[0-9*/,-]+ +[0-9*/,-]+ +[0-9*/,-]+ +[0-9*/,-]+ .*genreport' reports/crontab.txt 2>/dev/null; then
  echo "STEP:valid cron line for genreport:PASS"; else echo "STEP:valid cron line for genreport:FAIL:crontab.txt needs a 5-field schedule + genreport.sh"; fail=1; fi
exit $fail
""",
    solution="""#!/bin/bash
set -euo pipefail
mkdir -p /root/reports
n=$(find /root/data -maxdepth 1 -type f | wc -l)
echo "Files: $n" > "/root/reports/report-$(date +%F).txt"
echo "0 6 * * * /root/genreport.sh" > /root/reports/crontab.txt
""",
)

# ── 09 Admin menu ────────────────────────────────────────
proj(
    dir="09-admin-menu", id="proj-linux-adminmenu",
    title="Project: Interactive Admin Menu", minutes=45, points=250,
    prereq="[proj-linux-cronreport]",
    theory="""# Project: Interactive Admin Menu

A classic menu-driven admin tool: print options, read a choice, act, loop until
quit. Practises `while`/`case` and reading stdin (`read`).
""",
    instructions="""# Project Tasks

Write `/root/admin.sh` — a loop that prints a menu and reads a choice each time:

- `1` → print a line starting with `System time:` followed by the date
- `2` → print a line starting with `Disk usage:` followed by `df` output
- `3` → print a line starting with `Hostname:` followed by the hostname
- `q` → quit

The menu listing must show the options (include `1)` and a quit hint). It must
read choices from **stdin** so it can be scripted, e.g.
`printf '1\\nq\\n' | ./admin.sh`. Then click **Check**.
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -f admin.sh
exit 0
""",
    validate="""#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0
[ -x ./admin.sh ] || { echo "STEP:admin.sh exists:FAIL:create executable /root/admin.sh"; exit 1; }
echo "STEP:admin.sh exists:PASS"
menu=$(printf 'q\\n' | ./admin.sh 2>/dev/null)
if echo "$menu" | grep -q "1)"; then echo "STEP:shows a menu:PASS"; else echo "STEP:shows a menu:FAIL:print a menu with options like 1)"; fail=1; fi
o1=$(printf '1\\nq\\n' | ./admin.sh 2>/dev/null)
if echo "$o1" | grep -q "System time:"; then echo "STEP:option 1 prints System time:PASS"; else echo "STEP:option 1 prints System time:FAIL:choice 1 should print 'System time:'"; fail=1; fi
o3=$(printf '3\\nq\\n' | ./admin.sh 2>/dev/null)
if echo "$o3" | grep -q "Hostname:"; then echo "STEP:option 3 prints Hostname:PASS"; else echo "STEP:option 3 prints Hostname:FAIL:choice 3 should print 'Hostname:'"; fail=1; fi
exit $fail
""",
    solution="""#!/bin/bash
set -uo pipefail
while true; do
  echo "=== Admin Menu ==="
  echo "1) System time"
  echo "2) Disk usage"
  echo "3) Hostname"
  echo "q) Quit"
  read -r choice || break
  case "$choice" in
    1) echo "System time: $(date)" ;;
    2) echo "Disk usage: $(df -h / | awk 'NR==2{print $5}')" ;;
    3) echo "Hostname: $(hostname)" ;;
    q|Q) break ;;
    *) echo "unknown choice" ;;
  esac
done
""",
)

# ── 10 Bootstrapper ──────────────────────────────────────
proj(
    dir="10-bootstrapper", id="proj-linux-bootstrap",
    title="Project: Project Bootstrapper", minutes=50, points=300,
    prereq="[proj-linux-adminmenu]",
    theory="""# Project: Project Bootstrapper

Scaffold a fresh project from a template: create the directory layout, a README,
and an `installed.txt` derived from a package manifest. Ties together
everything: args, loops, file I/O, `mkdir -p`.
""",
    instructions="""# Project Tasks

`setup.sh` created `/root/packages.txt` (one package per line). Write
`/root/bootstrap.sh <name>` that scaffolds `/root/<name>/`:

1. Create the directories `src/`, `bin/`, and `config/` under `/root/<name>/`.
2. Write `/root/<name>/README.md` whose first line contains the project `<name>`.
3. Read `/root/packages.txt` and write `/root/<name>/installed.txt` with one
   line per package, each formatted `installed: <package>`.

Run `./bootstrap.sh myapp`, then click **Check** (the checker uses `myapp`).
""",
    setup="""#!/bin/sh
cd /root || exit 0
rm -rf myapp
cat > packages.txt <<'EOF'
curl
git
jq
EOF
exit 0
""",
    validate="""#!/bin/sh
cd /root 2>/dev/null || cd / 2>/dev/null
fail=0
[ -x ./bootstrap.sh ] || { echo "STEP:bootstrap.sh exists:FAIL:create executable /root/bootstrap.sh"; exit 1; }
echo "STEP:bootstrap.sh exists:PASS"
rm -rf myapp
./bootstrap.sh myapp >/dev/null 2>&1
if [ -d myapp/src ] && [ -d myapp/bin ] && [ -d myapp/config ]; then echo "STEP:creates src/bin/config:PASS"; else echo "STEP:creates src/bin/config:FAIL:missing directories"; fail=1; fi
if [ -f myapp/README.md ] && head -1 myapp/README.md | grep -q "myapp"; then echo "STEP:README mentions project name:PASS"; else echo "STEP:README mentions project name:FAIL:README.md first line should contain myapp"; fail=1; fi
ic=$(grep -c '^installed: ' myapp/installed.txt 2>/dev/null)
if [ "${ic:-0}" = "3" ] && grep -q '^installed: jq' myapp/installed.txt; then echo "STEP:installed.txt lists packages:PASS"; else echo "STEP:installed.txt lists packages:FAIL:need 3 'installed: <pkg>' lines"; fail=1; fi
exit $fail
""",
    solution="""#!/bin/bash
set -euo pipefail
name="${1:?usage: bootstrap.sh <name>}"
base="/root/$name"
mkdir -p "$base/src" "$base/bin" "$base/config"
echo "# $name" > "$base/README.md"
echo "Bootstrapped project." >> "$base/README.md"
: > "$base/installed.txt"
while IFS= read -r pkg; do
  [ -n "$pkg" ] && echo "installed: $pkg" >> "$base/installed.txt"
done < /root/packages.txt
""",
)


def write_exec(path: Path, content: str):
    path.write_text(content, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def main():
    for p in PROJECTS:
        d = BASE / p["dir"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "project.yaml").write_text(
            f"id: {p['id']}\n"
            f"title: \"{p['title']}\"\n"
            f"track: linux\n"
            f"level: beginner\n"
            f"estimated_minutes: {p['minutes']}\n"
            f"image: lab-linux:latest\n"
            f"prerequisites: {p['prereq']}\n"
            f"points: {p['points']}\n",
            encoding="utf-8",
        )
        (d / "theory.md").write_text(p["theory"], encoding="utf-8")
        (d / "instructions.md").write_text(p["instructions"], encoding="utf-8")
        write_exec(d / "setup.sh", p["setup"])
        write_exec(d / "validate.sh", p["validate"])
        # solution.md wraps the reference script in a bash block
        (d / "solution.md").write_text(
            "# Solution\n\n```bash\n" + p["solution"].strip() + "\n```\n",
            encoding="utf-8",
        )
        # also drop the raw reference script for the test harness
        write_exec(d / ".solution.sh", p["solution"])
    print(f"Wrote {len(PROJECTS)} projects to {BASE}")


if __name__ == "__main__":
    main()
