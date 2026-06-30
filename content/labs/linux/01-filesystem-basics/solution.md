# Solution

```bash
cd /root

# 1. Project tree
mkdir -p project/src project/docs

# 2. README
echo "hello" > project/README.md

# 3. Executable script (755)
echo '#!/bin/bash' > project/src/run.sh
chmod 755 project/src/run.sh

# 4. Owner-only secret (600)
echo "supersecret" > project/secret.txt
chmod 600 project/secret.txt
```

Verify with `ls -l project project/src`.
