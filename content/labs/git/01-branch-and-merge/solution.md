# Solution

```bash
cd /root/repo

# 1. Baseline on main
echo "v1" > app.txt
git add app.txt && git commit -m "baseline v1"

# 2. Feature branch
git switch -c feature

# 3. Commit on feature
echo "hello feature" > feature.txt
git add feature.txt && git commit -m "add feature"

# 4. Merge back
git switch main
git merge feature

git log --oneline --graph --all
ls   # app.txt and feature.txt both present
```
