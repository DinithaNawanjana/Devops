# Project Tasks

Write `/root/watch.sh`. On each run it must:

1. Check whether `/root/run/service.up` exists (the "service is running" marker).
2. **If missing** — recreate it and append a line containing `restart` to
   `/root/run/watch.log`.
3. **If present** — append a line containing `ok` to `/root/run/watch.log`.

The checker will delete the marker, run your script (expecting a restart), then
run it again (expecting ok). Click **Check** when ready.
