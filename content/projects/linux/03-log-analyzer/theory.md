# Project: Log File Analyzer

Parse a web access log with `grep`/`awk`/`sort`/`uniq` and emit a report:
total requests, error count, and the busiest client IPs. This is the bread and
butter of incident triage.

Key recipe — top N by frequency:

```bash
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -3
```
