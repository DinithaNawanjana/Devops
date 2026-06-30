# Deep Dive: Globbing & Parameter Expansion

## The problem
A directory full of mixed files is the perfect playground for two Bash
superpowers: **globbing** (matching filenames) and **parameter expansion**
(string surgery without calling external tools).

## Extracting an extension
```bash
ext="${f##*.}"     # strip the longest leading match up to the last dot
```
- `${var##pattern}` removes the **longest** prefix matching `pattern`.
- `${var#pattern}` removes the **shortest**.
- `${var%pattern}` / `${var%%pattern}` do the same from the **end**.

Knowing these four saves you from spawning `basename`, `dirname`, `cut`, or
`sed` in a loop — faster and with no quoting surprises.

## Looping over files safely
```bash
for f in *; do [ -f "$f" ] || continue; ...; done
```
- The `[ -f "$f" ]` guard skips directories (including the ones you're creating).
- Always quote `"$f"` — filenames can contain spaces, and unquoted expansion
  re-splits them.
- Handle the no-extension case (`"$ext" = "$f"` means no dot was found).

## Common pitfalls
- Re-picking moved files: if you `mv` files into a subdir of the same directory
  you're iterating, re-globbing can re-pick them. Snapshot the list or guard by
  type.
- Files beginning with `.` are skipped by default globs (`shopt -s dotglob`).
- Spaces/newlines in names — quoting and `-f` checks handle the common cases.

## Real-world
The same expansions power log-shipping scripts, media organizers, build
artifact sorters, and the rename logic in dotfiles managers.
