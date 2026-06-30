# Project Tasks

`setup.sh` made `/root/deploy/` with `blue/` and `green/` releases and a
`current` symlink pointing at `blue`. Write `/root/deploy/bluegreen.sh` that:

1. Reads which color `current` points at.
2. **Switches** `current` to the *other* color (blue↔green), atomically
   (`ln -sfn`).
3. Appends a line to `/root/deploy/switch.log`.

Running it once should flip `blue → green`; running again flips back. Click **Check**.
