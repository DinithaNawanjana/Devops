# Project: Disk Usage Alert

Read the root filesystem usage from `df` and raise an alert when it crosses a
threshold. Practises `df` parsing, numeric comparison, and logging.

```bash
df -P / | awk 'NR==2{gsub("%","",$5); print $5}'   # usage as a number
```
