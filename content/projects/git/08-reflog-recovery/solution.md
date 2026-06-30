# Solution

```bash
cd /root/repo
# Find the dropped commit in the reflog and restore its file.
lost=$(git reflog | grep -m1 "add lost" | awk '{print $1}')
git checkout "$lost" -- lost.txt
git add lost.txt
git commit -qm "restore: recover lost.txt via reflog"
```
