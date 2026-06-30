# Linux Filesystem, Files & Permissions

Everything in Linux is a file — including directories and devices. Files live
in a single tree rooted at `/`.

## Key directories

| Path     | Purpose                                |
|----------|----------------------------------------|
| `/home`  | User home directories                  |
| `/etc`   | System-wide configuration              |
| `/var`   | Variable data (logs, spool)            |
| `/tmp`   | Temporary files                        |
| `/usr`   | User programs and libraries            |

## Navigating & manipulating

- `pwd` — print working directory
- `ls -l` — list with details (permissions, owner, size)
- `mkdir -p a/b/c` — create nested directories
- `touch file` — create an empty file
- `cp`, `mv`, `rm` — copy, move, remove

## Permissions

`ls -l` shows a 10-character mode string like `-rwxr-xr--`:

```
-  rwx  r-x  r--
│   │    │    └── others: read
│   │    └─────── group:  read, execute
│   └──────────── owner:  read, write, execute
└──────────────── type:   - file, d directory, l symlink
```

Change permissions with `chmod`:

- Symbolic: `chmod u+x script.sh` (add execute for owner)
- Octal: `chmod 755 script.sh` (rwx r-x r-x)

The octal digits map to: read=4, write=2, execute=1.
So `755` = `7 (4+2+1)`, `5 (4+1)`, `5 (4+1)`.
