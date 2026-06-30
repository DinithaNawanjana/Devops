# Project Tasks

Write `/root/diskalert.sh <threshold>` that:

1. Reads the **current `/` usage percentage** from `df`.
2. If usage **> threshold**, writes `ALERT` (plus the percentage) to
   `/root/alert.txt`; otherwise writes `OK`.
3. **Appends a line to `/root/alert.log`** on every run.

Test both branches: `./diskalert.sh 0` (should ALERT) and
`./diskalert.sh 100` (should be OK). Then click **Check**.
