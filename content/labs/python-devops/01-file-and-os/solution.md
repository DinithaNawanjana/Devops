# Solution

```bash
cat > /root/analyze.py <<'PY'
#!/usr/bin/env python3
import json
from collections import Counter

statuses = Counter()
paths = Counter()
total = 0

with open("/root/access.log") as f:
    for line in f:
        parts = line.split()
        if len(parts) < 4:
            continue
        total += 1
        _ip, _method, path, status = parts[0], parts[1], parts[2], parts[3]
        statuses[status] += 1
        paths[path] += 1

summary = {
    "total": total,
    "by_status": dict(statuses),
    "top_path": paths.most_common(1)[0][0],
}

with open("/root/summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print(json.dumps(summary, indent=2))
PY

python3 /root/analyze.py
cat /root/summary.json
```
