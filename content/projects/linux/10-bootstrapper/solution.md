# Solution

```bash
#!/bin/bash
set -euo pipefail
name="${1:?usage: bootstrap.sh <name>}"
base="/root/$name"
mkdir -p "$base/src" "$base/bin" "$base/config"
echo "# $name" > "$base/README.md"
echo "Bootstrapped project." >> "$base/README.md"
: > "$base/installed.txt"
while IFS= read -r pkg; do
  [ -n "$pkg" ] && echo "installed: $pkg" >> "$base/installed.txt"
done < /root/packages.txt
```
