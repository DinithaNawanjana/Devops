# Solution

```bash
cd /root/repo
cat > changelog.sh <<'GEN'
#!/bin/bash
set -euo pipefail
echo "# Changelog" > CHANGELOG.md
git log --pretty='- %s' >> CHANGELOG.md
GEN
chmod +x changelog.sh
./changelog.sh
```
