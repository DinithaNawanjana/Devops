# Deep Dive: Project Scaffolding & Bootstrapping

## What "bootstrapping" means
Turning a bare machine (or empty directory) into a known-good starting state:
the right directory layout, baseline files, and declared dependencies. Doing
this *as code* makes environments reproducible — the same idea that grows into
Terraform, cloud-init, and `create-react-app`.

## Driving from a manifest
Reading the package list from `packages.txt` instead of hard-coding it is the
key move: **data-driven** scripts separate *what* (the manifest) from *how* (the
script). Add a package by editing data, not logic.
```bash
while IFS= read -r pkg; do
  [ -n "$pkg" ] && install "$pkg"
done < packages.txt
```
- `IFS=` preserves leading/trailing whitespace in each line.
- `read -r` keeps backslashes literal.
- The `[ -n "$pkg" ]` guard skips blank lines.

## Idempotent scaffolding
`mkdir -p` creates the tree without erroring if it already exists, so the
bootstrapper is safe to re-run — a property every provisioning tool needs.

## Common pitfalls
- Word-splitting the manifest if you `for pkg in $(cat …)` (breaks on spaces and
  is slower). Prefer the `while read` loop.
- Not validating the target name (`${1:?usage}` gives a clean error).
- Overwriting an existing project without warning.

## Real-world
This is the essence of `cloud-init`, Dockerfile `RUN` setup blocks, dotfiles
installers, and scaffolding CLIs.
