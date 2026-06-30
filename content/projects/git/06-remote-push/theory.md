# Deep Dive: Remotes & the Distributed Model

## Distributed, not centralized
Every clone is a **full repository** with all history — there's no privileged
"server" in Git's design, only repos that agree to sync. A **remote** is just a
named URL of another repo (`origin` by convention).

## Bare repos
A **bare** repo (`git init --bare`) has no working tree — it's storage only.
That's why servers (and this lab's `remote.git`) are bare: you can't push to a
branch that's checked out in a working tree, but a bare repo has none.

## Push mechanics
`git push origin feature` uploads your `feature` commits and updates the
remote's `refs/heads/feature`. Tracking (`-u`) links your local branch to the
remote one so later `git push`/`pull` need no arguments.

## Pitfalls
- Pushing to a non-bare repo's checked-out branch → rejected.
- Diverged histories → push rejected ("fetch first"); resolve with pull/rebase.
- Force-pushing over a teammate's commits.

## Real-world
This is the foundation of the fork-and-pull-request workflow that powers all of
open source: fork (a server-side clone), push a branch, open a PR.
