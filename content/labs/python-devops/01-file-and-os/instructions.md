# Your Task

`setup.sh` placed a web log at `/root/access.log`. Each line is:

```
<ip> <method> <path> <status>
```

Write `/root/analyze.py` that reads the log and writes a JSON summary to
`/root/summary.json`.

Requirements — `summary.json` must contain:

1. **`total`** — the total number of log lines (an integer).

2. **`by_status`** — an object mapping each status code (as a string) to its
   count, e.g. `{"200": 3, "404": 1, "500": 1}`.

3. **`top_path`** — the single most frequently requested path (a string).

Run it with `python3 /root/analyze.py`, confirm `summary.json` looks right
(`cat /root/summary.json`), then click **Check**.

> Hints: `json` for output, `collections.Counter` for counting. Read the file
> with `open(...)` and `str.split()` each line.
