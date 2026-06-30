# Deep Dive: Log Analysis with the Unix Toolkit

## The pipeline mindset
Log analysis is the canonical demonstration of the Unix philosophy: chain
small, single-purpose filters with `|` and let each do one transform. You can
answer surprisingly deep questions about traffic, errors, and abuse with
`grep`, `awk`, `sort`, `uniq`, and `wc` — no database required.

## The building blocks
- **`awk '{print $N}'`** — split each line on whitespace and emit field *N*
  (the client IP is usually `$1` in access logs).
- **`sort | uniq -c`** — `uniq` only collapses *adjacent* duplicates, so you
  **must** `sort` first; `-c` prefixes each group with its count.
- **`sort -rn`** — sort those counts numerically, descending.
- **`head -n N`** — take the top N.

The famous "top talkers" recipe:
```bash
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -3
```

## Filtering for signal
- `grep -c ERROR` counts error lines without printing them.
- `awk '$9 ~ /^5/'` matches 5xx status codes by field, far more precise than a
  blind `grep 500` that also matches byte counts or URLs.

## Common pitfalls
- Forgetting to `sort` before `uniq -c` — you'll get fragmented, wrong counts.
- Whitespace vs. delimiter assumptions — combined log format quotes the request,
  so `$7` is the path only because the quotes are counted as fields. Know your
  log format.
- Huge files: prefer streaming (`awk`/`grep`) over loading into memory.

## Real-world
Every SRE triages incidents this way first. The same shapes become Loki/LogQL
queries, Elasticsearch aggregations, and Splunk searches — the tool changes, the
thinking doesn't.
