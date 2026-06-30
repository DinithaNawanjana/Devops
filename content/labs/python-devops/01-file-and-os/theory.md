# Files, OS & JSON in Python

Python is the glue language of DevOps — parsing logs, calling APIs, wrangling
config. This lab covers the everyday standard-library tools.

## Reading & writing files

```python
with open("input.txt") as f:
    for line in f:
        print(line.rstrip())

with open("output.txt", "w") as f:
    f.write("hello\n")
```

## The `os` module

```python
import os
os.getenv("HOME")            # environment variables
os.listdir(".")              # directory contents
os.makedirs("a/b", exist_ok=True)
```

## JSON

```python
import json
data = json.loads('{"name": "web", "replicas": 3}')
print(data["replicas"])               # 3
text = json.dumps(data, indent=2)     # back to a string
```

## Counting with collections

```python
from collections import Counter
Counter(["a", "b", "a"]).most_common(1)   # [('a', 2)]
```

A typical DevOps script: read a file → transform → write JSON. That's exactly
what you'll build here.
