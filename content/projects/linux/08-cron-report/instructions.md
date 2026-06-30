# Project Tasks

Write `/root/genreport.sh` that:

1. Creates `/root/reports/` and writes a dated report file
   `report-<YYYY-MM-DD>.txt` containing a line `Files: <N>` where `<N>` is the
   number of files in `/root/data/` (created by setup).
2. Writes a **valid cron line** to `/root/reports/crontab.txt` — five schedule
   fields followed by a command that mentions `genreport.sh` (e.g. run daily).

Run `./genreport.sh`, then click **Check**.
