# Solution

```bash
cd /root/repo
git merge feature || true          # conflicts on config.txt
echo "color=purple" > config.txt   # resolve
git add config.txt
git commit -qm "merge: resolve color to purple"
```
