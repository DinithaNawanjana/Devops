# Deep Dive: The Reflog — Git's Safety Net

## "Lost" almost never means lost
Git rarely deletes commits immediately. When you `reset --hard`, rebase, or
delete a branch, the commits become **unreferenced** (no branch points at them),
but they survive in the object database until garbage collection runs (default
~30 days for unreachable objects).

## The reflog
`git reflog` is a local journal of **everywhere HEAD has been** — every commit,
checkout, reset, and rebase, with entries like `HEAD@{2}`. It's how you find the
hash of a commit no branch points to anymore:
```bash
git reflog                       # find the lost commit's hash
git checkout <hash> -- file      # restore a file, or
git branch rescue <hash>         # recreate a branch at it
```

## Why it's local-only
The reflog is per-clone and never pushed — it reflects *your* HEAD's journey. So
recovery is something you do in the repo where the loss happened.

## Pitfalls
- Waiting too long — `git gc` eventually prunes truly unreachable objects.
- Confusing `reflog` (HEAD movements) with `log` (commit ancestry).

## Real-world
"I rebased and lost my work" is a daily Slack message; the reflog is the calm
answer. It's also how you undo a bad `reset --hard`.
