# Deep Dive: Rewriting History Cleanly

## Two audiences for history
While you work, commits are a *save button* ("wip", "fix typo"). When you share,
history is *documentation* for reviewers and future debuggers. Squashing turns
the former into the latter.

## Two ways to squash
1. **Interactive rebase**: `git rebase -i HEAD~3`, mark commits `squash`/`fixup`.
   Full control, can reorder/reword.
2. **Soft reset**: `git reset --soft HEAD~3 && git commit`. Moves the branch
   pointer back 3 commits but **keeps the index/working tree**, so one new commit
   captures all the changes. Simpler when you just want "combine the last N".

The working tree is identical either way — only the commit graph changes.

## The golden rule
**Never rewrite history that others have pulled.** Rewriting changes commit
hashes; collaborators who based work on the old hashes get a divergent mess.
Squash *before* pushing, or only on branches you own.

## Pitfalls
- Force-pushing a rewritten shared branch (`--force-with-lease` is safer than
  `--force`, but communication is safest).
- Squashing away a commit you needed to revert independently.

## Real-world
"Squash and merge" is a one-click button on GitHub PRs precisely because clean,
atomic commits make `git bisect`, `revert`, and code archaeology sane.
