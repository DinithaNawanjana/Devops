# Project Tasks

`/root/lib.git` is a bare library repo. In the app repo `/root/app`:

1. Add `/root/lib.git` as a **submodule** at path **`vendor/lib`**.
2. Commit the result.

> Adding a submodule from a local path may need
> `git -c protocol.file.allow=always submodule add …`.

Click **Check**.
