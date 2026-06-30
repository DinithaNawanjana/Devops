# Your Task

Work in `/root/repo` (created for you, already `git init`-ed on `main`).

1. **Make a baseline commit**

   Create `app.txt` with the text `v1`, then commit it on `main`.

   ```bash
   cd /root/repo
   echo "v1" > app.txt
   git add app.txt && git commit -m "baseline v1"
   ```

2. **Create a feature branch**

   Create and switch to a branch named `feature`.

   ```bash
   git switch -c feature
   ```

3. **Commit on the feature branch**

   Add a new file `feature.txt` containing `hello feature`, and commit it on
   `feature`.

4. **Merge back into main**

   Switch to `main` and merge `feature` into it. Afterwards, both `app.txt`
   and `feature.txt` must exist on `main`.

Click **Check** when done.
