#!/bin/bash
set -e
cd /root/repo
cat > .git/hooks/pre-commit <<'HOOK'
#!/bin/sh
if git diff --cached | grep -q "TODO"; then
  echo "pre-commit: TODO found, blocking commit"
  exit 1
fi
exit 0
HOOK
chmod +x .git/hooks/pre-commit
echo "clean code" > a.txt; git add a.txt; git commit -qm "add a"
echo "TODO: finish" > b.txt; git add b.txt; git commit -qm "add b" || true
