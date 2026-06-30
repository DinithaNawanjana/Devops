# Pipes, Filters & Redirection

The Unix philosophy: small tools that do one thing well, combined with pipes.

## Redirection

- `cmd > file` — write stdout to `file` (overwrite)
- `cmd >> file` — append stdout to `file`
- `cmd < file` — read stdin from `file`
- `cmd 2> err.log` — redirect stderr

## Pipes

`|` connects the stdout of one command to the stdin of the next:

```bash
cat access.log | grep "ERROR" | wc -l
```

## Essential filters

| Tool   | Does                                          |
|--------|-----------------------------------------------|
| `grep` | Filter lines matching a pattern               |
| `sort` | Sort lines                                    |
| `uniq` | Collapse adjacent duplicates (`-c` to count)  |
| `wc`   | Count lines/words/bytes (`-l` for lines)      |
| `cut`  | Extract columns (`-d` delimiter, `-f` field)  |
| `awk`  | Field-oriented processing                     |
| `sed`  | Stream editing / substitution                 |

## A classic recipe: top N most frequent

```bash
sort file | uniq -c | sort -rn | head -n 5
```
