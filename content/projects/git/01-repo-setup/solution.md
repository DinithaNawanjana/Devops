# Solution

```bash
cd /root/repo
printf 'node_modules/\n*.log\n' > .gitignore
echo "# My Project" > README.md
git add .gitignore README.md
git commit -qm "chore: initial project scaffold"
git branch develop
```
