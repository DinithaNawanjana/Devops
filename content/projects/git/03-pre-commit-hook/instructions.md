# Project Tasks

In `/root/repo`:

1. Install an executable **`.git/hooks/pre-commit`** that **blocks** a commit if
   any staged change contains the text `TODO`.
2. Prove it: commit a clean file `a.txt` (should succeed), then try to commit a
   file `b.txt` containing `TODO` (should be rejected, so `b.txt` never lands).

Click **Check**.
