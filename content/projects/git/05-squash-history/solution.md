# Solution

```bash
cd /root/repo
# Recombine the last 3 commits into one (keeps the working tree/content).
git reset --soft HEAD~3
git commit -qm "feat: add feature"
```
