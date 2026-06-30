# Deep Dive: Submodules & Vendoring

## The problem they solve
Sometimes a repo needs another repo inside it — a shared library, a theme, a
vendored dependency — pinned to a **specific commit**, not just "latest". A
submodule embeds repo B inside repo A at a fixed SHA.

## How they're recorded
`git submodule add <url> <path>` does three things: clones B into `path`, writes
a `.gitmodules` file (the URL + path mapping), and stages a special **gitlink**
entry that records B's exact commit. Cloning A later needs
`git submodule update --init` to populate the submodule.

## The trade-off
Submodules give **reproducibility** (exact pinned commit) but add friction:
contributors must know the extra commands, and updating the pin is a manual
commit in A. Alternatives: subtree merges, or a package manager.

## Pitfalls
- Cloning without `--recurse-submodules` → empty submodule directories.
- Forgetting to commit the updated gitlink after changing the submodule.
- The local-path/file-protocol restriction (`protocol.file.allow`) on recent
  Git for security.

## Real-world
Used for shared CI config, design systems, firmware blobs, and any "pin an exact
upstream commit" need.
