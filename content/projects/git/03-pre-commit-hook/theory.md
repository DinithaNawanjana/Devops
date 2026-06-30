# Deep Dive: Git Hooks

## Shifting feedback left
A bug caught at commit time costs seconds; the same bug caught in CI costs
minutes; in production, hours. **Hooks** are scripts Git runs at lifecycle
points so you can catch problems at the earliest possible moment.

## Where hooks live
`.git/hooks/` holds them. `pre-commit` runs *before* the commit is created — exit
non-zero and the commit is **aborted**. Other useful ones: `commit-msg`
(enforce message format), `pre-push` (run tests before sharing).

## Anatomy
```sh
#!/bin/sh
if git diff --cached | grep -q "TODO"; then
  echo "blocked: remove TODOs"; exit 1
fi
```
`git diff --cached` is the **staged** content — exactly what's about to be
committed. That's what you lint.

## The catch: hooks aren't shared
`.git/hooks/` is **not** part of the repo, so teammates don't get your hook
automatically. Real teams use a manager (the `pre-commit` framework, Husky) that
installs hooks from a committed config.

## Pitfalls
- Hooks that are slow make people `--no-verify` and bypass them.
- Forgetting `chmod +x` — a non-executable hook is silently skipped.

## Real-world
Linters, formatters (Prettier/Black), secret scanners, and conventional-commit
checks all run as hooks before CI ever sees the code.
